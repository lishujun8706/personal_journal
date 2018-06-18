class SelfDefine(object):
    def process_request(self,request):
        #Todo
        print("this is process_request")
    def process_view(self, request, fnc, arg, kwarg):
        #Todo
        print("This is process_view")
    def process_response(self,request,response):
        #Todo
        print("this is process_response")
        return response
    def process_exception(self,request,exception):
        #Todo
        print("this is process_exception")
    def process_template_response(self):
        print("this is process_template_response")
        pass