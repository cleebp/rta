"""analyser.py

Based on Anna Wszeborowska's implementation here: https://github.com/aniawsz/rtmonoaudio2midi/blob/master/audiostream.py
"""
import itertools
from collections import deque

import numpy as np
from pygame import display, surfarray

from config import *


class Analyser:
    FREQUENCY_RANGE = (500, 1200)

    def __init__(self, screen, window_size=None, segments_buf=None):
        self.screen_array = np.zeros((SCREEN_SIZE, SCREEN_SIZE))
        self.screen = screen

        if window_size is None:
            window_size = WINDOW_SIZE
        self._window_size = window_size

        if segments_buf is None:
            segments_buf = int(SAMPLE_RATE / window_size)
        self._segments_buf = segments_buf

        self._thresholding_window_size = THRESHOLD_WINDOW_SIZE
        assert self._thresholding_window_size <= segments_buf

        self._last_spectrum = np.zeros(window_size, dtype=np.float32)
        self._last_flux = deque(
            np.zeros(segments_buf, dtype=np.float32), segments_buf)
        self._last_prunned_flux = 0

        self._hanning_window = np.hanning(window_size)
        # The zeros which will be used to double each segment size
        self._inner_pad = np.zeros(window_size)

        # To ignore the first peak just after starting the application
        self._first_peak = True

    def _get_flux_for_thresholding(self):
        return list(itertools.islice(
            self._last_flux,
            self._segments_buf - self._thresholding_window_size,
            self._segments_buf))

    def find_onset(self, spectrum):
        """
        Calculates the difference between the current and last spectrum,
        then applies a thresholding function and checks if a peak occurred.
        """
        last_spectrum = self._last_spectrum
        flux = sum([max(spectrum[n] - last_spectrum[n], 0)
                    for n in range(self._window_size)])
        self._last_flux.append(flux)

        thresholded = np.mean(
            self._get_flux_for_thresholding()) * THRESHOLD_MULTIPLIER
        prunned = flux - thresholded if thresholded <= flux else 0
        peak = prunned if prunned > self._last_prunned_flux else 0
        self._last_prunned_flux = prunned
        return peak

    def find_fundamental_freq(self, samples):
        cepstrum = self.cepstrum(samples)
        # search for maximum between 0.08ms (=1200Hz) and 2ms (=500Hz)
        # as it's about the recorder's frequency range of one octave
        min_freq, max_freq = self.FREQUENCY_RANGE
        start = int(SAMPLE_RATE / max_freq)
        end = int(SAMPLE_RATE / min_freq)
        narrowed_cepstrum = cepstrum[start:end]

        peak_ix = narrowed_cepstrum.argmax()
        freq0 = SAMPLE_RATE / (start + peak_ix)

        if freq0 < min_freq or freq0 > max_freq:
            # Ignore the note out of the desired frequency range
            return

        return freq0

    def process_data(self, data):
        spectrum = self.autopower_spectrum(data)
        print('Spectrum:', spectrum)
        for i in range(len(spectrum)):
            self.screen_array.fill(i)
            surfarray.blit_array(self.screen, self.screen_array)
            display.flip()

        # screen.blit(surf, (0,0))
        # pygame.display.flip()

        onset = self.find_onset(spectrum)
        self._last_spectrum = spectrum

        if self._first_peak:
            self._first_peak = False
            return

        if onset:
            freq = self.find_fundamental_freq(data)
            return freq

    def autopower_spectrum(self, samples):
        """
        Calculates a power spectrum of the given data using the Hamming window.
        """
        # TODO: check the length of given samples; treat differently if not
        # equal to the window size

        windowed = samples * self._hanning_window
        # Add 0s to double the length of the data
        padded = np.append(windowed, self._inner_pad)
        # Take the Fourier Transform and scale by the number of samples
        spectrum = np.fft.fft(padded) / self._window_size
        autopower = np.abs(spectrum * np.conj(spectrum))
        return autopower[:self._window_size]

    def cepstrum(self, samples):
        """
        Calculates the complex cepstrum of a real sequence.
        """
        spectrum = np.fft.fft(samples)
        log_spectrum = np.log(np.abs(spectrum))
        cepstrum = np.fft.ifft(log_spectrum).real
        return cepstrum