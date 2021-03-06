from pytest import fixture
from tak_env import space
from tak_env.types import Stone, Direction
import numpy as np

def describe_move():
  @fixture
  def state():
    return np.array([
      [
        [0,0,0],
        [0,0,0],
        [2,0,0],
      ],
      [
        [0,0,0],
        [0,0,0],
        [1,0,0],
      ],
      [
        [0,0,0],
        [0,0,0],
        [1,0,0],
      ]
    ])
  
  def should_apply_each_move_part(state):
    assert space.move(state, {
      'action': 'move',
      'carry': (2, 1),
      'from': (2, 0),
      'direction': '>',
    }).tolist() == [
      # TODO remove empty layer?
      [
        [0,0,0],
        [0,0,0],
        [0,0,0],
      ],
      [
        [0,0,0],
        [0,0,0],
        [0,1,0],
      ],
      [
        [0,0,0],
        [0,0,0],
        [0,1,2],
      ]
    ]

def describe_is_valid_move_part():
  @fixture
  def state():
    return np.array([
      [
        [1,0,0],
        [2,0,0],
        [1,0,0],
      ],
      [
        [-1,0,-3],
        [-1,0,-1],
        [-1,-1,-2],
      ],
      [
        [1,0,2],
        [1,0,1],
        [1,1,2],
      ],
      [
        [1,0,2],
        [1,0,1],
        [1,1,2],
      ]
    ])

  def it_is_valid_to_move_onto_empty(state):
    assert space.is_valid_move_part(state, (1,1), [1]) == True

  def it_is_valid_to_move_onto_flat(state):
    assert space.is_valid_move_part(state, (0,0), [1]) == True

  def it_is_not_valid_to_move_onto_standing(state):
    assert space.is_valid_move_part(state, (1,0), [1]) == False

  def it_is_valid_to_move_onto_standing_if_captital(state):
    assert space.is_valid_move_part(state, (1,0), [-3]) == True

  def it_is_not_valid_to_move_onto_capital(state):
    assert space.is_valid_move_part(state, (0,2), [1]) == False

def describe_get_partitions():
  def it_returns_permutations_that_add_up_to_n():
    assert(list(space.get_partitions(2))) == [(1, 1), (2,)]
    assert(list(space.get_partitions(3))) == [(1, 1, 1), (1, 2), (2, 1), (3,)]
    assert(list(space.get_partitions(4))) == [(1, 1, 1, 1), (1, 1, 2), (1, 2, 1), (1, 3), (2, 1, 1), (2, 2), (3, 1), (4,)]

def describe_get_carry_partitions():
  def it_combines_partitions_up_to_limit():
    assert(list(space.get_carry_partitions(3))) == [(1,), (1, 1), (2,), (1, 1, 1), (1, 2), (2, 1), (3,)]

def describe_combinations():
  def it_creates_possible_combinations_of_parameters():
    assert space.get_combinations({
      'action': ['move'],
      'carry': space.get_partitions(3),
      'direction': [Direction.LEFT.value],
      'from': [(0,1)],
    }) == [
      {'action': 'move', 'carry': (1, 1, 1), 'direction': '<', 'from': (0, 1)},
      {'action': 'move', 'carry': (1, 2), 'direction': '<', 'from': (0, 1)},
      {'action': 'move', 'carry': (2, 1), 'direction': '<', 'from': (0, 1)},
      {'action': 'move', 'carry': (3,), 'direction': '<', 'from': (0, 1)}
    ]