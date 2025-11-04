class ScoreUtils:
    def normalize_score(self, score, min_val=0, max_val=1):
        # Stub: Normalize score to 0-1
        return max(min(score, max_val), min_val)
