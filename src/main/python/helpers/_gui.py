from fbs_runtime.application_context.PyQt5 import ApplicationContext


class UI:
    def get_design(resouce_name):
        appctxt = ApplicationContext()
        ret = appctxt.get_resource(resouce_name)
        return ret
