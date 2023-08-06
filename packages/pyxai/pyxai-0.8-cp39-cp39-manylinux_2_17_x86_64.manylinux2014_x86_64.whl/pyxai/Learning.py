

from operator import index
from pyxai.source.learning.MLSolver import MLSolverInformation, MLSolver
from pyxai.source.learning.scikitlearn import Scikitlearn
from pyxai.source.learning.xgboost import Xgboost
from pyxai.source.learning.generic import Generic


from pyxai.source.core.structure.type import EvaluationMethod, EvaluationOutput, Indexes, SaveFormat

import json 


HOLD_OUT = EvaluationMethod.HoldOut
LEAVE_ONE_GROUP_OUT = EvaluationMethod.LeaveOneGroupOut
K_FOLDS = EvaluationMethod.KFolds

DT = EvaluationOutput.DT
RF = EvaluationOutput.RF
BT = EvaluationOutput.BT
SAVE = EvaluationOutput.SAVE

TRAINING = Indexes.Training
TEST = Indexes.Test
MIXED = Indexes.Mixed
ALL = Indexes.All

RAW_DATA = SaveFormat.RawData
SOLVER_SPECIFIC = SaveFormat.SolverSpecific

def load(models_directory):
  solver = MLSolver()
  files = solver.load_get_files(models_directory)
  solver_names = []
  for _, model in enumerate(files):
    model_file, map_file = model
    f = open(map_file)
    data = json.loads(json.load(f))
    solver_names.append(data['solver_name']) 
    f.close()
  assert all(solver_name == solver_names[-1] for solver_name in solver_names), "All solver names have to be the same !"
  
  if solver_names[0] == Generic().get_solver_name():
    solver = Generic()
  elif solver_names[0] == Xgboost().get_solver_name():
    solver = Xgboost()
  elif solver_names[0] == Scikitlearn().get_solver_name():
    solver = Scikitlearn()
  else:
    assert False, "Bad solver names in the directory: " + models_directory

  models = solver.load(models_directory=models_directory)
  return solver, models
