import pyomo.environ as pyo
import pandas as pd
import sys
from pyomo.opt import SolverStatus, TerminationCondition

def feasible_model():
    """ This function builds an abstract model of the utility exchange network """
    model = pyo.AbstractModel()
    # ##########################
    # SETS
    # ##########################
    model.COAL = pyo.Set(doc='Set of coalitions')
    model.PLAYER = pyo.Set(doc='Set of players')
    model.PLAYER_SUB = pyo.Set(model.COAL, doc='Player subsets')
    # ##########################
    # VARIABLES
    # ##########################
    model.xj = pyo.Var(model.PLAYER, within=pyo.NonNegativeReals, doc='allocation to player i')
    model.nu = pyo.Var(within=pyo.Reals, doc='nu parameter for minmax core')
    model.eps = pyo.Var(within=pyo.Reals, doc='epsilon parameter for least core')
    # ##########################
    # PARAMETERS
    # ##########################
    model.value = pyo.Param(model.COAL, mutable=True, doc='value of each coalition')
    model.gc = pyo.Param(mutable=True, doc='value of grand coalition')
    # ##########################
    # CONSTRAINTS
    # ##########################
    model.INCREASE = pyo.Constraint(model.COAL, rule=lambda model, i: sum(model.xj[j] for j in model.PLAYER_SUB[i]) >= model.nu*model.value[i]-model.eps)
    model.EFFICIENCY = pyo.Constraint(rule=lambda model: sum(model.xj[j] for j in model.PLAYER) == model.gc)
    model.EPS_CONST = pyo.Constraint(rule=lambda model: model.eps == 0)
    model.NU_CONST = pyo.Constraint(rule=lambda model: model.nu == 1)
    # ##########################
    # OBJECTIVE FUNCTION
    # ##########################
    model.OBJ1 = pyo.Objective(sense=pyo.minimize, rule=lambda model: sum(model.xj[j] for j in model.PLAYER))
    model.OBJ2 = pyo.Objective(sense=pyo.minimize, rule=lambda model: model.eps)
    model.OBJ3 = pyo.Objective(sense=pyo.maximize, rule=lambda model: model.nu)
    return model

def instantiate(model_data):
    """ This function builds an instance of the optimization model with specific data and objective function

    Parameters:
    ------------
    ecoopt_data:  Dictionary with parameters that populate the model
    OBJECTIVE:    Objective function
    """
    model = feasible_model()
    problem = model.create_instance(model_data, report_timing=False)
    return problem


def solve_model(instance, GAMS, options=False):
    """ This function solves the instance of the optimization model

    Parameters:
    ------------
    GAMS_PATH:   GAMS directory
    """
    # Solver set-up:
    if GAMS is False:
        solver = pyo.SolverFactory('glpk')
        results = solver.solve(instance)
    else:
        solver = pyo.SolverFactory('gams')
        io_options = dict()                                 # Set MILP solver options:
        #io_options['mtype'] ="milp"                           # - type of problem (lp, nlp, mip, minlp)
        io_options['solver'] = 'CPLEX'                      # - name of solver
        #io_options['symbolic_solver_labels']=True           # - use full Pyomo component names rather than shortened symbols
        #io_options['skip_trivial_constraints']=False
        if options == False:
            options = ['option optcr = 0.000000001; \n' 'option reslim = ' + str(3600) + ';\nGAMS_MODEL.optfile = 1;',
             '$onecho > cplex.opt', 'workmem=4096 \nscaind=1 \nnumericalemphasis=1 \nepmrk=0.9 \neprhs=1E-9', '$offecho']
        results = solver.solve(instance, keepfiles=True, tee=False, report_timing=False, io_options=io_options, add_options = options) # Solve model
    instance.solutions.load_from(results)
    return results, instance

def create_model_data(game):
    game['coalition'] = [tuple(x) for x in game['coalition']]
    game = game.set_index('coalition')
    PLAYER = list(set([element for sublist in [i for i in game.index] for element in sublist]))
    COAL = [str(coal) for coal in game.index if str(coal) if str(coal) not in ['()'] and len(coal) < len(PLAYER)]
    PLAYER_SUB = {str(coal): list(eval(coal)) for coal in COAL}
    value = {str(coal): game['value'][eval(coal)] for coal in COAL}
    gc = {None: max(game['value'])}
    model_data = {None: {
        'COAL': COAL,
        'PLAYER': PLAYER,
        'PLAYER_SUB': PLAYER_SUB,
        'value': value,
        'gc': gc,
    }}
    return model_data

def core_exists(game, GAMS=False):
    model_data = create_model_data(game)
    instance = instantiate(model_data)
    instance.OBJ1.activate()
    instance.OBJ2.deactivate()
    instance.OBJ3.deactivate()
    results, instance_solved = solve_model(instance, GAMS)
    if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
        print('The set of core allocations is NOT EMPTY\n')
        return True
    else:
        print('WARNING: The set of core allocations is EMPTY (!!!)\n')
        return False

def is_in_core(game, x):
    if round(sum(x[p] for p in x),8) != round(max(game['value']),8):
        return False
    for ind in game.index:
        if sum(x[p] for p in game['coalition'][ind]) < game['value'][ind]:
            return False
    return True

def least_core(game, GAMS=False):
    model_data = create_model_data(game)
    instance = instantiate(model_data)
    instance.OBJ1.deactivate()
    instance.OBJ2.activate()
    instance.OBJ3.deactivate()
    instance.EPS_CONST.deactivate()
    results, instance_solved = solve_model(instance, GAMS)
    eps = instance_solved.OBJ2()
    if eps <= 0:
        print('The core is not empty and epsilon is ' + str(eps) + '\n')
    else:
        print('The core is empty and epsilon is ' + str(eps) + '\n')
    return {j: instance_solved.xj[j].value for j in instance.PLAYER}

def minmax_core(game, GAMS=False):
    model_data = create_model_data(game)
    instance = instantiate(model_data)
    instance.OBJ1.deactivate()
    instance.OBJ2.deactivate()
    instance.OBJ3.activate()
    instance.NU_CONST.deactivate()
    results, instance_solved = solve_model(instance, GAMS)
    nu = instance_solved.OBJ3()
    if nu >= 1:
        print('The core is not empty and epsilon is ' + str(nu) + '\n')
    else:
        print('The core is empty and epsilon is ' + str(nu) + '\n')
    return {j: instance_solved.xj[j].value for j in instance.PLAYER}