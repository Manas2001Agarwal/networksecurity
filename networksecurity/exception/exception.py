import sys
class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys): # type: ignore
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()
        self.lineno = exc_tb.tb_lineno # type: ignore
        self.file = exc_tb.tb_frame.f_code.co_filename # type: ignore
        
    def __str__(self):
        return f"Error occured in file {self.file} , line no {self.lineno} with error_message {self.error_message}"

if __name__ == "__main__":
    try:
        a = 1/0
        print("this will not be printed")
    except Exception as e:
        NetworkSecurityException(e,sys) 