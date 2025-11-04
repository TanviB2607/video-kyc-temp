class DecisionEngine:
    def decide(self, S_face, S_live_p, S_live_a, S_doc, S_docmatch):
        if S_face >= 0.82 and S_live_p >= 0.75 and S_live_a >= 0.70 and S_doc >= 0.80 and S_docmatch >= 0.95:
            return "APPROVED"
        elif S_face >= 0.75 or S_live_p >= 0.70 or S_live_a >= 0.65 or S_doc >= 0.75 or S_docmatch >= 0.90:
            return "REVIEW"
        else:
            return "REJECTED"
