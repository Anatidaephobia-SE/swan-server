class request_checker_response:
    def __init__(self, have_all, error_message):
        self.have_all = have_all
        self.error_message = error_message

# This function check if request have given parameters or not
# And return a tuple if request have all given parameters first item will be True
# Second item is string to return in JsonResponse
def have_parameters(request, *parameters):
    ex_params = []
    for param in parameters:
        if not(param in request.data.keys()):
            ex_params.append(param)
    response = ''
    for param in ex_params:
        response += (param)
        if ex_params.index(param) != len(ex_params) - 1: response += ', '
    response += ' parameter(s) are required'
    return request_checker_response(len(ex_params) == 0, response)

def have_queryparams(request, *queryparams):
    ex_params = []
    for param in queryparams:
        if not(param in request.query_params.keys()):
            ex_params.append(param)
    response = ''
    for param in ex_params:
        response += (param)
        if ex_params.index(param) != len(ex_params) - 1: response += ', '
    response += ' query param(s) are required'
    return request_checker_response(len(ex_params) == 0, response)