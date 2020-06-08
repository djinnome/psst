
from pyomo.environ import SolverFactory
import warnings
import os
from .results import PSSTResults


PSST_WARNING = os.getenv('PSST_WARNING', 'ignore')


def solve_model(model, solver='glpk', solver_io=None, keepfiles=True, verbose=True, symbolic_solver_labels=True, is_mip=True, **kwargs):
    if solver == 'xpress':
        solver = SolverFactory(solver, solver_io=solver_io, is_mip=is_mip)
    else:
        solver = SolverFactory(solver, solver_io=solver_io)
    model.preprocess()
    if is_mip and solver=='scip':
        if 'solver_options' in kwargs:
            if 'limits/gap' in kwargs['solver_options']:
                solver.options['limits/gap']=float(kwargs['solver_options']['limits/gap'])

    if solver=='gurobi':
        if 'solver_options' in kwargs:
            if 'MIPGap' in kwargs['solver_options']:
                solver.options['MIPGap'] = float(kwargs['solver_options']['MIPGap'])
            if 'TimeLimit' in kwargs['solver_options']:
                solver.options['TimeLimit'] = float(kwargs['solver_options']['TimeLimit'])
    with warnings.catch_warnings():
        warnings.simplefilter(PSST_WARNING)
        solver.solve(model, suffixes=['dual'], tee=verbose, keepfiles=keepfiles, symbolic_solver_labels=symbolic_solver_labels)

    return model
