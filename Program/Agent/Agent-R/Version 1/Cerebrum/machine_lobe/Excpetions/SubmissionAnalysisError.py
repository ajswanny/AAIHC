class SubmissionAnalysisError(BaseException):


    def __init__(self):

        print(
            " ----------------------------------------------------------\n",
            "Encountered Submission analysis error. Possible reasons: ",
            "\n",
            "\tIndico IO API Unknown Error.\n",
            "----------------------------------------------------------"
        )

