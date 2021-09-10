button = None


dType.SetIOMultiplexingExtEx(api, 10, 3, 1)
button = dType.GetIODIExt(api, 10)[0]
if (dType.GetIODIExt(api, 10)[0]) == 0:
  print('Button is not pressed')
while True:
  print('waiting...')
  if (dType.GetIODIExt(api, 10)[0]) == 1:
    print('Button was pressed. Now exiting...')
    break
