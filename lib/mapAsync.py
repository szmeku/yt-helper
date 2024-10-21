from lib.applyInParallelWithErrorHandling import applyInParallelWithErrorHandling

def mapAsync(funcToApply):

    def _f(items):
        return list(applyInParallelWithErrorHandling(funcToApply, items))

    return _f


