## Basic abstractions

1. Controller. Controller is a main python code that store credential information and directly connect to your github organization and monitor for any github actions that request runner with specific labels
2. Provider. Provider is a specific piece of code that you can modulary add to controller to support specific type of self-hosted runners. it has pre-define RPC class so controller can do requests via it and get results. Provider stores connection logic and runner creation under the hood and controller just requests from it (like vagrant works)

## TODO

1. Define structure.
   1. credentials
   2. communication
   3. classes
   4. logic
   5. api interactions
   6. configuration
2. Decide are providers gonna be separate containers/repositories/folders/python modules etc
3. Develop basic provider
4. (Optional) implement additional logic to support additional configuration/ multiple providers, labels limits etc.
