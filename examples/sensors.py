from dji_asdk_to_python.products.aircraft import Aircraft
APP_IP = "192.168.100.206"

aircraft = Aircraft(APP_IP)
fc = aircraft.getFlightController()
res = fc.setCollisionAvoidanceEnabled(True)
print(res)