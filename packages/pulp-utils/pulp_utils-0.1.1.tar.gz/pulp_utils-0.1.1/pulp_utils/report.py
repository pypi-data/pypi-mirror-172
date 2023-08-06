from pulp import LpStatus

__all__ = ['report_result']


def report_result(model):
    result = {
        "solver": model.solver.name,
        "status": LpStatus[model.status],
        "optimization_result": {
            model.objective.name: model.objective.value()
        },
        "constraint_sensitivity": [{'name': name, 'constraint': c, 'shadow_price': c.pi, 'slack': c.slack} for name, c in model.constraints.items()]
    }
    for v in model.variables(): 
        result["optimization_result"][v.name] = v.varValue
    return result
