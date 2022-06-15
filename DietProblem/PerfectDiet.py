from pyomo.core import *
from pyomo.environ import *

model = AbstractModel()
model.foods = Set()
model.nutrients = Set()
model.costs = Param(model.foods)
model.min_nutrient = Param(model.nutrients)
model.max_nutrient = Param(model.nutrients)
model.volumes = Param(model.foods)
model.max_volume = Param()
model.nutrient_value = Param(model.nutrients, model.foods)

model.amount = Var(model.foods, within=NonNegativeReals)


def totalcost(model):
    return sum(model.costs[n] * model.amount[n] for n in model.foods)


model.totalcost = Objective(rule=totalcost)


def maxvolume(model):
    return sum(model.volumes[n] * model.amount[n] for n in model.foods) <= model.max_volume


model.maxvol = Constraint(rule=maxvolume)


def nutrientrule(model, n):
    value = sum(model.nutrient_value[n, f] * model.amount[f] for f in model.foods)

    return model.min_nutrient[n], value, model.max_nutrient[n]


model.nutrientconstraint = Constraint(model.nutrients, rule=nutrientrule)

instance = model.create_instance('DietProblem.dat')
opt = SolverFactory('glpk')
results = opt.solve(instance)

print(results)

print([value(instance.amount[f]) for f in instance.foods])
