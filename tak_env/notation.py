from string import ascii_lowercase
from tak_env.types import Direction, Stone, StoneLetter

def to_ptn(action, size):
  if action.get('action') == 'move':
    space_from = get_square(action.get('from'), size)
    carry = ''.join([str(x) for x in action.get('carry')])
    direction = action.get('direction')
    return f'{space_from}{direction}{carry}'

  space_to = get_square(action.get('to'), size)
  piece = get_letter_value(action.get('piece'))
  return f'{piece}{space_to}'
  
def to_action(ptn, size):
  ptn = standardize(ptn)
  direction = get_movement_direction(ptn)

  if direction:
    space_from, carry = ptn.split(direction)
    space_from = get_space(space_from[-2:], size)
    carry = tuple([int(x) for x in carry])

    return {
      'action': 'move',
      'carry': carry,
      'from': space_from,
      'direction': direction,
    }

  return { 
    'action': 'place',
    'to': get_space(ptn[-2:], size),
    'piece': get_stone_value(ptn[0])
  }

def standardize(ptn):
  direction = get_movement_direction(ptn)
  if direction:
    # omitted first character assumes 1 stone moved
    if not ptn[0].isdigit():
      ptn = '1' + ptn
    # omitted carry assumes total carry
    parts = ptn.split(direction)
    if not parts[1]:
      ptn = ptn + ptn[0]
    if ptn[-1:] == StoneLetter.CAPITAL.value:
      ptn = ptn[:-1]
  else:
    # omitted first character assumes flat stone
    if not any(ptn[0] in x for x in [
      StoneLetter.CAPITAL.value,
      StoneLetter.FLAT.value,
      StoneLetter.STANDING.value,
    ]):
      ptn = StoneLetter.FLAT.value + ptn
  return ptn

def get_stone_value(letter):
  if letter == StoneLetter.FLAT.value:
    return Stone.FLAT.value
  if letter == StoneLetter.STANDING.value:
    return Stone.STANDING.value
  if letter == StoneLetter.CAPITAL.value:
    return Stone.CAPITAL.value
  return None

def get_letter_value(stone):
  if stone == Stone.FLAT.value:
    return StoneLetter.FLAT.value
  if stone == Stone.STANDING.value:
    return StoneLetter.STANDING.value
  if stone == Stone.CAPITAL.value:
    return StoneLetter.CAPITAL.value
  return None

def get_movement_direction(ptn):
  if Direction.UP.value in ptn:
    return Direction.UP.value
  if Direction.DOWN.value in ptn:
    return Direction.DOWN.value
  if Direction.LEFT.value in ptn:
    return Direction.LEFT.value
  if Direction.RIGHT.value in ptn:
    return Direction.RIGHT.value
  return None

def get_square(space, size):
  r, c = space
  return '{letter}{number}'.format(letter=ascii_lowercase[c], number=size-r)

def get_space(square, size):
  letter, number = square
  return (
     size - int(number),
     ascii_lowercase.index(letter)
  )
