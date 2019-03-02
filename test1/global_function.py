import re

class CustomValidations:
    def titleValidation(self,string):
        regex = '^[_a-zA-Z-.,0-9]'
        if string=='null' or string=='undefined' or len(string)==0:
            return 1
        match = re.match(regex, string)
        if match is None:
            return 0
        else:
            return 2

    def dataValidation(request, string, stringReguired, int, intRequired):
        status = 0
        msg = None
        for i in range(0, len(string)):
            if string[i] not in request.POST:
                msg = 'Please enter ' + string[i]
                status = 0
                return msg, status
            else:
                variable = request.POST[string[i]]
                status1 = CustomValidations.titleValidation(request, variable)
                if status1 == 0:
                    msg = 'Special character are not allowed in ' + string[i]
                    status = 0
                    return msg, status
        for i in range(0, len(stringReguired)):
            if stringReguired[i] not in request.POST:
                msg = 'Please enter ' + stringReguired[i]
                status = 0
                return msg, status
            else:
                variable = request.POST[stringReguired[i]]
                status1 = CustomValidations.titleValidation(request, variable)
                if status1 == 0:
                    msg = 'Special character are not allowed in ' + stringReguired[i]
                    status = 0
                    return msg, status
                elif status1 == 1:
                    msg = 'Please enter ' + stringReguired[i]
                    status = 0
                    return msg, status
        for i in range(0, len(int)):
            if int[i] not in request.POST:
                msg = 'Please enter ' + int[i]
                status = 0
                return msg, status
            else:
                variable = request.POST[int[i]]
                status1 = CustomValidations.intValidation(request, variable)
                if status1 == 0:
                    msg = 'Please enter integer value in ' + int[i]
                    status = 0
                    return msg, status
        for i in range(0, len(intRequired)):
            if intRequired[i] not in request.POST:
                msg = 'Please enter ' + intRequired[i]
                status = 0
                return msg, status
            else:
                variable = request.POST[intRequired[i]]
                status1 = CustomValidations.intValidation(request, variable)
                if status1 == 0:
                    msg = 'Please enter integer value in ' + intRequired[i]
                    status = 0
                    return msg, status
                elif status1 == 1:
                    msg = 'Please enter integer value in ' + intRequired[i]
                    status = 0
                    return msg, status

        status = 1
        msg = 'success'
        return msg, status