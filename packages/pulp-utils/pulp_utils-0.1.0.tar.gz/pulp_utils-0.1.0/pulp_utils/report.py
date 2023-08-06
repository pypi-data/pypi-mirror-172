from pulp import LpStatus

__all__ = ['report_result']


def report_result(model):
    result = {
        "solver": model.solver.name,
        "status": LpStatus[model.status],
        model.objective.name: model.objective.value()
    }
    for v in model.variables(): 
        result[v.name] = v.varValue
    return result
