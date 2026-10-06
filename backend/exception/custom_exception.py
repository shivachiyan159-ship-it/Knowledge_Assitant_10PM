import sys
import traceback
from backend.logger import GLOBAL_LOGGER as log


class CustomException(Exception):
    def __init__(self, error_message, error_detail=None):
        # normalize message
        normal_message = str(error_message)

        exc_type = exc_value = exc_tb = None

        # cheking exception types
        if error_detail is None:
            exc_type, exc_value, exc_tb = sys.exc_info()
        else:
            if hasattr(error_detail, "exc_info"):
                exc_type, exc_value, exc_tb = error_detail.exc_info()
            elif isinstance(error_detail, BaseException):
                exc_type, exc_value, exc_tb = type(
                    error_detail), error_detail, error_detail.__traceback__
            else:
                exc_type, exc_value, exc_tb = sys.exc_info()

        # walk through last trace back
        last_tb = exc_tb
        while last_tb and last_tb.tb_next:
            last_tb = last_tb.tb_next

        # setting all properties from lasttrace back

        self.filename = last_tb.tb_frame.f_code.co_filename
        self.lineno = last_tb.tb_lineno
        self.error_message = normal_message

        if exc_type and exc_tb:
            self.traceback_str = " ".join(
                traceback.format_exception(*sys.exc_info()))
        else:
            self.traceback_str = ""

        super().__init__(self.__str__())

    def __str__(self):
        return f"""
                Error in [{self.filename}] at line [{self.lineno}]
                Message: {self.error_message}
                Traceback: {self.traceback_str}
            """


try:
    a = 2/0
    # we can call apis
    # we can read files

except Exception as e:
    # print(e)
    log.error(CustomException("zero divison error", sys.exc_info()))

# if __name__ == "__main__":
#     try:
#         a = 2/0
#         # we can call apis
#         # we can read files

#     except Exception as e:
#         # print(e)
#         log.error(CustomException("zero divison error", sys.exc_info()))

#         # CustomException("zero divison error")

#         # CustomException("zero divison error", e)

#         # CustomException("zero divison error", sys)

#         # CustomException("zero divison error", sys.exc_info())

#         # trc_bk=["lofginmethod","validate","authenticate","testmethod"]
