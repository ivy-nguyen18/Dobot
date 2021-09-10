count = None
input2 = None

"""Describe this function...
"""
def button():
  global count, input2
  dType.SetIOMultiplexingExtEx(api, 10, 3, 1)
  print(dType.GetIODIExt(api, 10)[0])
  dType.dSleep(10000)
  count = 0
  while True:
    input2 = dType.GetIODIExt(api, 10)[0]
    if press() == 10:
      break
  print('Ending')
  print(count)

"""Describe this function...
"""
def new():
  print('Starting...')

"""Describe this function...
"""
def press():
  global input2, count
  if input2 == 1:
    print('Button Pressed')
    count = count + 1
  return count


new()
button()
