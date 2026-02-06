import numpy as np
import pandas as pd


def adaptive_trend(
    df: pd.DataFrame, window: int, column: str, stability_threshold: float
):
    """
    Refactor of Josep's 'sliding_window_analysis' (tendencies.ipynb) function
    Adapts window size based on signal stability
    """

    signal = df[column].values
    N = len(signal)

    # Initialize arrays
    spacial_means = np.full(N, np.nan)
    definitive_means = np.full(N, np.nan)
    definitive_stds = np.full(N, np.nan)

    if window % 2 == 0:
        raise ValueError("window must be odd.")

    space = window // 2
    window_amplification = 0

    # Iterate through signal (preserving teammate's logic)
    for i in range(space, N - space):
        local_window = signal[i - space : i + space + 1]
        mean_window = np.mean(local_window)

        spacial_means[i] = mean_window

        # Check stability
        if i > space and abs(spacial_means[i - 1] - mean_window) < stability_threshold:
            window_amplification += 1
        else:
            # Stability broken, finalize the segment
            start_segment = i - 1 - window_amplification
            end_segment = i + space

            # Ensure indices are within bounds
            start_segment = max(0, start_segment)
            end_segment = min(N, end_segment)

            global_window = signal[start_segment:end_segment]
            if len(global_window) > 0:
                definitive_means[start_segment:end_segment] = np.mean(global_window)
                definitive_stds[start_segment:end_segment] = np.std(global_window)

            window_amplification = 0

    # Handle the final segment
    end_idx = N - 1
    start_idx = end_idx - window_amplification
    if start_idx < N:
        definitive_means[start_idx:] = spacial_means[start_idx:]
        definitive_stds[start_idx:] = 0  # Fallback for end

    # Return as DataFrame
    return pd.DataFrame(
        {"adaptive_mean": definitive_means, "adaptive_std": definitive_stds},
        index=df.index,
    )
