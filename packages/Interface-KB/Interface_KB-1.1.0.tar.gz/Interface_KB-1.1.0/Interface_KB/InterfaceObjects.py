import json

#TODO: discuss these interface objects as there are the main API interfacing mechanisms

class ASG():
    """
        ASG: Class representing the Assembly Sequence Generation (ASG) algorithm

         :param string Name: Name of the ASG
         :param string Description: Description of the ASG
         :param enum ProcessingType: ProcessingType of the ASGASG
         :param list Generator: Generator description of the ASG
         :param list Selector: Selector description of the ASG
         :param list Evaluator: Evaluator description of the ASG
         :param list StopConditionList: StopConditionList description of the ASG
         :param objectlist SelectorDFARuleList: list of DFA rules linked to the ASG selector
         :param objectlist EvaluatorDFARuleList: list of DFA rules linked to the ASG evaluator
    """
    def __init__(self,JSONDescriptor=None,Name="",Description="",ProcessingType="Full",Generator=[],Selector=[],SelectorDFARules = [],Evaluator=[],EvaluatorDFARules = [],StopConditions=[],DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.ProcessingType = str(ProcessingType)   #TODO: ENUM not serializable!
            #ASG GENERATOR config
            self.Generator = Generator
            # ASG SELECTOR config
            self.Selector = Selector
            self.SelectorDFARuleList = SelectorDFARules
            # ASG EVALUATOR config
            self.Evaluator = Evaluator
            self.EvaluatorDFARuleList = EvaluatorDFARules
            # ASG Terminator config
            self.StopConditionList=StopConditions
        else:
            self.json2object(JSONDescriptor)
            x=10

    def json2object(self,jsonDescriptor):
        """
             Function to generate a ASG object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the DFA rule

        """
        #--interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)
        #--setup object--
        self.Name = jsonObject['Name']
        self.Description = jsonObject['Description']
        self.ProcessingType = jsonObject['ProcessingType']
        self.Generator = jsonObject['Generator']
        self.Selector = jsonObject['Selector']
        self.Evaluator = jsonObject['Evaluator']
        self.Generator = jsonObject['Generator']
        self.StopConditionList = []
        for terminator in jsonObject['StopConditionList']:
            s = StopCondition(None, terminator['Name'], terminator['Description'],terminator['Value'], terminator['StopCriteria'])
            self.StopConditionList.append(s)
        #TODO: discuss if we need to add the rules at once?


    def object2json(self):
        """
            Function to generate a json file from the ASG
        """
        return json.dumps(self, default=lambda o: o.__dict__,indent=4)

    def object2yaml(self):
        """
            Function to generate a yaml file from the ASG - PROTOTYPE
        """
        return -1 #yaml.dump(self,indent=4)

class ASGAlgorithmData():
    """
            ASGAlgorithmData: Class representing the (performance)data for a given ASG algorithm

             :param double Score: Score of the ASG algorithm
             :param boolean Feasible: is feasible indication of the ASG algorithm
             :param string UnexploredOptions: Unexplored options of the ASG algorithm
             :param double Priority: Priority of the ASG algorithm

        """
    def __init__(self,JSONDescriptor=None,Score=0.0,Feasible=False,UnexploredOptions="",Priority=1.0,DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Score = Score
            self.Feasible = Feasible
            self.UnexploredOptions = UnexploredOptions
            self.Priority = Priority
        else:
            self.json2object(JSONDescriptor)
            x=10

    def json2object(self,jsonDescriptor):
        """
             Function to generate a ASG algorithm data object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the DFA rule

        """
        #--interpret JSON file--
        x=1

    def object2json(self):
        """
            Function to generate a json file from the ASG algorithm dta
        """
        return json.dumps(self, default=lambda o: o.__dict__,indent=4)

class DFARule():
    """
        DFARule: Class representing the DFA rule

         :param string Name: Name of the DFA rule
         :param string Description: Description of the DFA rule
         :param string RuleType: RuleType of the DFA rule
         :param bool isAppliedToProduct: Identify if DFA rule is applied to product
         :param bool isAppliedToProductPart: Identify if DFA rule is applied to product part
         :param bool isAppliedToAssemblySequence: Identify if DFA rule is applied to assembly sequence
         :param enum hasScorePropagation: hasScorePropagation of the DFA rule
         :param enum hasScoreType: hasScoreType of the DFA rule
         :param objectlist optionList: List of options of the DFA rule
         :param object property: Referenced property of the DFA rule
         :param list preprocessedData: preprocessedData of the DFA rule

    """
    def __init__(self, JSONDescriptor=None, Name="", Description="", RuleType='',isAppliedToProduct=False, isAppliedToProductPart=False,isAppliedToAssemblySequence=False,hasScorePropagation="ScorePropagation=Best",hasScoreType="ScoreType=Score",preprocessedData=[],optionList = [], DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.RuleType = RuleType
            self.isAppliedToProduct = isAppliedToProduct
            self.isAppliedToProductPart = isAppliedToProductPart
            self.isAppliedToAssemblySequence = isAppliedToAssemblySequence
            self.hasScorePropagation = str(hasScorePropagation)
            self.hasScoreType=str(hasScoreType)
            self.optionList = optionList
            self.property = None
            self.preprocessedData = preprocessedData
        else:
            # TODO: import json descriptor to setup object
            self.json2object(JSONDescriptor)

    def json2object(self,jsonDescriptor):
        """
             Function to generate a DFA object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the DFA rule

        """
        #--interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)
        #--setup object--
        self.Name = jsonObject['DFARule']['Name']
        self.Description = jsonObject['DFARule']['Description']
        self.RuleType = jsonObject['DFARule']['RuleType']
        if 'True' in jsonObject['DFARule']['isAppliedToProduct']:self.isAppliedToProduct = True
        else:self.isAppliedToProduct = False
        if 'True' in jsonObject['DFARule']['isAppliedToProductPart']:self.isAppliedToProductPart = True
        else:self.isAppliedToProductPart = False
        if 'True' in jsonObject['DFARule']['isAppliedToAssemblySequence']:self.isAppliedToAssemblySequence = True
        else:self.isAppliedToAssemblySequence = False
        if '1' in jsonObject['DFARule']['hasScorePropagation']:self.hasScorePropagation = 1
        else:self.hasScorePropagation = 0
        if '1' in jsonObject['DFARule']['hasScoreType']:self.hasScoreType = 1
        else:self.hasScoreType = 0
        self.optionList = []
        for option in jsonObject['DFARule']['optionList']:
            temp = []
            temp.append(option['Name'])
            temp.append(option['Value1'])
            temp.append(option['Value2'])
            self.optionList.append(temp)
        for property in jsonObject['DFARule']['property']:
            temp = []
            temp.append(property['Name'])
            temp.append(property['Value1'])
            temp.append(property['Value2'])
            self.property=temp

        #self.preprocessedData = preprocessedData       #TODO!


    def object2json(self):
        """
            Function to generate a json file from the DFA rule
        """
        return json.dumps(self.__dict__,indent=4)

class PerformanceModel():
    """
       PerformanceModel: Class representing the complete performance model

        :param string Name: Name of the performance model
        :param string Description: Description of the performance model
        :param list OptimizationMethod: OptimizationMethod of the performance model
        :param objectlist StopConditionList: List of stop conditions
        :param list MethodPerformance: List of stop performance metrics
        :param list RAWResults: List of RAW optimization results
        :param list interpretedResults: List of interpreted optimization results
        :param objectlist parameterList: list of linked parameters
        :param objectlist ObjectiveList: list of optimization objectives
        :param objectlist ConstraintList: list of optimization constraints
    """
    def __init__(self, JSONDescriptor=None, Name="", Description="",OptimizationMethod=None,MethodPerformance=[],RAWResults=[],parameterlist = [],StopConditions = [],ObjectiveList=[],ConstraintList=[],interpretedResults=[],DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            #OptimizationMethod + Stop
            self.OptimizationMethod = OptimizationMethod
            self.StopConditionList = StopConditions
            # OptimizationResult
            self.MethodPerformance = MethodPerformance
            self.RAWResults = RAWResults
            self.interpretedResults=interpretedResults
            #parameter list
            self.parameterList = parameterlist
            # DESIGN TARGETS
            self.ObjectiveList = ObjectiveList
            self.ConstraintList = ConstraintList

        else:
            # TODO: import json descriptor to setup object
            self.json2object(JSONDescriptor)

    def json2object(self, jsonDescriptor):
        """
             Function to generate a performance model from a JSON file

             :param string jsonDescriptor: absolute path to the json file for performance model

        """
        # --interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)
        # --setup object--
        self.Name = jsonObject['Name']
        self.Description = jsonObject['Description']
        self.OptimizationMethod = [jsonObject['OptimizationMethod'][0],jsonObject['OptimizationMethod'][1],jsonObject['OptimizationMethod'][2]]
        #stopConditions
        self.StopConditionList = []
        for stp in jsonObject["StopConditionList"]:
            stopC = StopCondition(Name=stp["Name"],Description=stp["Description"],Value=stp["Value"],Stopcriteria=stp["StopCriteria"])
            self.StopConditionList.append(stopC)

        #Method results TODO: this is not complete yet
        self.MethodPerformance = jsonObject['MethodPerformance']
        self.RAWResults = jsonObject['RAWResults']
        self.interpretedResults = jsonObject['interpretedResults']

        # DecisionVariables
        self.parameterList = []
        for var in jsonObject["parameterList"]:
            pList = []
            for p in var["parameterList"]:
                par = Parameter(Name=p["Name"], Description=p["Description"],Key=p["Key"],GUID=p["GUID"], Value=p["Value"], Stopcriteria=p["StopCriteria"],Unit=p["Unit"])
                pList.append(par)
            decisionvariable = DecisionVariable(Name=var["Name"], Description=var["Description"], InitialValue=var["InitialValue"],MinValue=var["MinValue"], MaxValue=var["MaxValue"], Optimum=var["Optimum"],Resolution = var["Resolution"],parameters=pList)
            self.parameterList.append(decisionvariable)

        # Objectives
        self.ObjectiveList = []
        for objective in jsonObject["ObjectiveList"]:
            if len(objective["ObjectiveTerm"])==3:
                term = Term(None,Value=[objective["ObjectiveTerm"][0],objective["ObjectiveTerm"][1],objective["ObjectiveTerm"][2]])
            else:
                term = Term(None, Value=objective["ObjectiveTerm"][0])  # if string or float
            obj_ = Objective(Name=objective["Name"], Description=objective["Description"], ObjectiveOption=objective["ObjectiveOption"],ObjectiveTerm=term)
            self.ObjectiveList.append(obj_)

        # Constraints
        self.ConstraintList = []
        for cnstr in jsonObject["ConstraintList"]:
            if len(cnstr["Expression"][0]) == 4:
                Lterm = Term(None,Value=[cnstr["Expression"][0][1],cnstr["Expression"][0][2],cnstr["Expression"][0][3]])
            else:
                Lterm = Term(None, Value=cnstr["Expression"][0][1])  # if string or float
            if len(cnstr["Expression"][1]) == 4:
                Rterm = Term(None,Value=[cnstr["Expression"][1][1], cnstr["Expression"][1][2], cnstr["Expression"][1][3]])
            else:
                Rterm = Term(None, Value=cnstr["Expression"][1][1])  # if string or float
            operator = cnstr["Expression"][2]
            expression = Expression(JSONDescriptor=None,LeftTerm=Lterm,ExpressionOperator=operator,RightTerm=Rterm)
            cnstr_ = Constraint(Name=cnstr["Name"], Description=cnstr["Description"],Expression=expression)
            self.ConstraintList.append(cnstr_)

    def clean(self):
        self.parameterList = []
        # DESIGN TARGETS
        self.ObjectiveList = []
        self.ConstraintList = []

    def object2json(self):
        """
               Function to generate a json file from the performance model
        """
        return json.dumps(self, default=lambda o: o.__dict__,indent=4)

class StopCondition():
    """
        StopCondition: Class representing the algorithm stop conditions

         :param string Name: Name of the object
         :param string Description: Description of the object
         :param string Value: Value of the object
         :param enum StopCriteria: StopCriteria of the object

    """
    def __init__(self, JSONDescriptor=None, Name="", Description="", Value=0.0, Stopcriteria="maxDepth=0", DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.Value = Value
            self.StopCriteria = Stopcriteria
        else:
            # TODO: import json descriptor to setup object
            x = 10

class Parameter():
    """
            Parameter: Class representing the parameter

             :param string Name: Name of the parameter
             :param string Description: Description of the parameter
             :param string Key: Key of the parameter
             :param string GUID: Global unique identifier of the parameter
             :param float Value: Value of the parameter
             :param string Unit: Unit of measurement of the parameter
             :param enum StopCriteria: StopCriteria of the parameter
    """
    def __init__(self, JSONDescriptor=None, Name="", Description="",Key="",GUID="", Value=0.0, Stopcriteria="maxDepth=0",Unit="", DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.Key = Key
            self.GUID = GUID
            self.Value = Value
            self.StopCriteria = Stopcriteria
            self.Unit=Unit
        else:
            # TODO: import json descriptor to setup object
            x = 1

class Objective():
    """
        Objective: Class representing the optimization Objective

         :param string Name: Name of the Objective
         :param string Description: Description of the Objective
         :param enum ObjectiveOption: ObjectiveOption of the Objective
    """
    def __init__(self, JSONDescriptor=None, Name="", Description="",ObjectiveTerm=None,ObjectiveOption="Minimize", DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.ObjectiveTerm = ObjectiveTerm      #Added 18/10/2022 meeting Pavel
            self.ObjectiveOption = ObjectiveOption

        else:
            # TODO: import json descriptor to setup object
            x = 10

class Constraint():
    """
        Constraint: Class representing the optimization Constraint

         :param string Name: Name of the constraint
         :param string Description: Description of the constraint
         :param list Expression: Expression of the constraint
    """
    def __init__(self, JSONDescriptor=None, Name="", Description="",Expression=None, DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.Expression = Expression

        else:
            # TODO: import json descriptor to setup object
            x = 10

#----------------------Added 18/10/2022 meeting Pavel--------------------------
class Term():
    """
        Term: Class representing a Term of an expression

         :param string|float|object Value: Value of the term (different datatypes: string|float|object)
    """
    def __init__(self, JSONDescriptor=None, Value=None, DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Value = Value


        else:
            # TODO: import json descriptor to setup object
            x = 10

class Expression():
    """
        Expression: Class representing an expression

         :param object LeftTerm: LeftTerm of the expression (can also be an expression)
         :param string ExpressionOperator: Expression operator value e.g. "+"
         :param object RightTerm: RightTerm of the expression (can also be an expression)
    """
    def __init__(self, JSONDescriptor=None, LeftTerm=None, ExpressionOperator="+",RightTerm=None, DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.LeftTerm = LeftTerm
            self.ExpressionOperator = ExpressionOperator
            self.RightTerm = RightTerm

        else:
            # TODO: import json descriptor to setup object
            x = 10

class OptimizationMethod():
    """
        Term: Class representing an optimization method

         :param string Name: Name of the OptimizationMethod
         :param string Description: Description of the OptimizationMethod
         :param string OptimizationAlgorithmClass: Class of the OptimizationMethod ("Heuristic"|"Deterministic"|"Metaheuristic")
         :param list OptionList: List of options for the OptimizationMethod
    """
    def __init__(self, JSONDescriptor=None, Name="", Description="",OptimizationAlgorithmClass="Heuristic",OptionList=[], DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.OptimizationAlgorithmClass = OptimizationAlgorithmClass
            self.OptionList = OptionList

        else:
            # TODO: import json descriptor to setup object
            x = 10

class Option():
    """
        Option: Class representing an option

         :param string Name: Name of the Option
         :param string|boolean|float|object|list|[hasX,hasY,hasZ]|("AddingIsWorse"|"ConstantSurfaceOnly") Value: Value of the term (different datatypes: string|boolean|float|object|list|[hasX,hasY,hasZ]|("AddingIsWorse"|"ConstantSurfaceOnly"))
    """
    def __init__(self, JSONDescriptor=None, Name="",Value=None, DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Value = Value


        else:
            # TODO: import json descriptor to setup object
            x = 10
#------------------------------------------------------------------------------
class DecisionVariable():
    """
        DecisionVariable: Class representing the optimization Objective

         :param string Name: Name of the DecisionVariable
         :param string Description: Description of the DecisionVariable
         :param float InitialValue: InitialValue of the DecisionVariable
         :param float MinValue: MinValue of the DecisionVariable
         :param float MaxValue: MaxValue of the DecisionVariable
         :param float Optimum: Optimum of the DecisionVariable
         :param float Resolution: Resolution of the DecisionVariable
         :param string Unit: Unit of measurement of the DecisionVariable
         :param objectlist parameterList: list of linked parameters
    """
    def __init__(self, JSONDescriptor=None, Name="", Description="",InitialValue=0.0,MinValue=0.0, MaxValue=0.0, Optimum=0.0,Resolution = 0.0,parameters=[],Unit="", DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.InitialValue = InitialValue
            self.MinValue = MinValue
            self.MaxValue = MaxValue
            self.Optimum = Optimum
            self.Resolution = Resolution
            self.parameterList = parameters
            self.Unit = Unit
        else:
            # TODO: import json descriptor to setup object
            x = 1

class Product():
    """
        Product: Class representing the Product

         :param string Name: Name of the Product
         :param string STEPFile: Absolute path to the Product STEP file
         :param objectlist parameterList: list of linked parameters
    """
    def __init__(self, JSONDescriptor=None, Name="", Description="",STEPFile='',parameters = [], DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.STEPFile = STEPFile
            self.parameterList = parameters

        else:
            self.json2object(JSONDescriptor)
            x = 10

    def json2object(self,jsonDescriptor):
        """
             Function to generate a Product object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the Product

        """
        #--interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)
        #--setup object--
        self.Name = jsonObject['Name']
        self.Description = jsonObject['Description']
        self.STEPFile = jsonObject['STEPFile']

        self.parameterList = []
        for par in jsonObject['parameterList']:
            p = Parameter(None, Name=par['Name'], Description=par['Description'],Key=par['Key'], GUID=par['GUID'],Value=par['Value'],Stopcriteria=par['StopCriteria'],Unit=par["Unit"])
            self.parameterList.append(p)
        #TODO: discuss if we need to add the rules at once?

    def object2json(self):
        """
               Function to generate a json file from the Product model
        """
        return json.dumps(self, default=lambda o: o.__dict__,indent=4)

class ProductPart():
    """
        Product: Class representing the Product Part

         :param string Name: Name of the Product
         :param string ProductType: Product part type
         :param int Quantity: Number of same product parts in product
         :param objectlist parameterList: list of linked parameters
         :param objectlist partList: list of linked product parts
         :param list material: list of the material properties
         :param boolean isFastner: identification if productpart is fastner
    """
    def __init__(self, JSONDescriptor=None, Name="", Description="",ProductType='',Quantity=0,parameters = [],partList=[],material = [],isFastner=False, DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.ProductType = ProductType
            self.Quantity = Quantity
            self.parameterList = parameters
            self.partList = partList
            self.material = material    #TODO: Stiffness not yet correct
            self.isFastner = isFastner

        else:
            self.json2object(JSONDescriptor)
            x = 10

    def json2object(self,jsonDescriptor):
        """
             Function to generate a ProductPart object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the ProductPart

        """

        #--interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)
        #--setup object--
        self.Name = jsonObject['Name']
        self.Description = jsonObject['Description']
        self.ProductType = jsonObject['ProductType']
        self.Quantity = jsonObject['Quantity']
        self.parameterList = []
        try:
            self.isFastner = jsonObject['isFastner']
        except:
            self.isFastner = False
        for par in jsonObject['parameterList']:
            p = Parameter(None, Name=par['Name'], Description=par['Description'], Key=par['Key'], GUID=par['GUID'],Value=par['Value'], Stopcriteria=par['StopCriteria'],Unit=par["Unit"])
            self.parameterList.append(p)
        self.partList = []
        for subPart in jsonObject['partList']:
            p = self.getInstance(subPart)
            self.partList.append(p)
        self.material = jsonObject['material']  # TODO: Stiffness not yet correct

    def object2json(self):
        """
               Function to generate a json file from the ProductPart model
        """
        return json.dumps(self, default=lambda o: o.__dict__,indent=4)

    def getInstance(self,subPart):
        """
               Function to fetch a ProductPart model recursively
        """
        part_temp = ProductPart(Name=subPart['Name'],Description=subPart['Description'],ProductType=subPart['ProductType'],Quantity=subPart['Quantity'])

        part_temp.parameterList = []
        for par in subPart['parameterList']:
            p = Parameter(None, Name=par['Name'], Description=par['Description'], Key=par['Key'], GUID=par['GUID'], Value=par['Value'], Stopcriteria=par['StopCriteria'],Unit=par["Unit"])
            part_temp.parameterList.append(p)
        part_temp.partList = []
        for subPart in subPart['partList']:
            p = self.getInstance(subPart)
            part_temp.partList.append(p)
        part_temp.material = subPart['material']  # TODO: Stiffness not yet correct
        return part_temp

class AssemblySequence():
    """
        Product: Class representing the AssemblySequence

         :param string Name: Name of the AssemblySequence
         :param string Description: Description of the AssemblySequence
         :param list AssemblyMetric: AssemblyMetric identification
         :param objectList assemblyOptions: list of assemblyOption objects
    """

    def __init__(self, JSONDescriptor=None, Name="", Description="", AssemblyMetric=[],AssemblyOptions=None, DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.AssemblyMetric = AssemblyMetric
            self.AssemblyOptions = AssemblyOptions

        else:
            self.rootAssembly=None
            self.childActive = False
            self.json2object(JSONDescriptor)
            x = 10

    def setAssemblyOption(self, Option):
        try:
            # operations
            operationList = []
            for operation in Option['Operations']:
                op = Operation(Name=operation['Name'], Description="NOT IN MM")
                op.OperationMetric = [operation['OperationMetric'][0], operation['OperationMetric'][1]]  # TODO: in MM, multiple metrics can be added -> is this necessary?
                # operators
                operatorList = []
                for operator in operation['Operators']:
                    operator_temp = Operator(Name=operator['Name'],CostPerHour=operator['CostPerHour'],Height=operator['Height'],MaxLiftingWeight=operator['MaxLiftingWeight'],Reach=operator['Reach'])
                    operatorList.append(operator_temp)
                op.Operators = operatorList
                # Tools
                ToolList = []
                for tool in operation['Tool']:
                    requiredOperators = []
                    for r_operator in operation['Operators']:
                        requiredOperators.append(r_operator['Name'])  # TODO: only name reference added, ok?
                    Tool_temp = Tool(Name=tool['Name'],Mass=tool['Mass'],Cost=tool['Cost'],Orientation=tool['Orientation'],Geometry=tool['Geometry'],RequiredOperators=requiredOperators)
                    #Tool_temp = [tool.hasName, tool.hasMass, tool.hasCost, tool.hasOrientation.hasData,tool.hasGeometry.hasDataInStepFile, requiredOperators]
                    ToolList.append(Tool_temp)
                op.Tool = ToolList
                # Fastners
                FastnersList = []
                for fastner in operation['Fastners']:
                    FastnersList.append(fastner[0])  # TODO: only name reference added, ok?
                op.Fastners = FastnersList
                operationList.append(op)

            # -- define the assemblyOption --
            ASO = AssemblyOption(Name=Option['Name'],Operations=operationList)

            #Linking the recursive operations!
            subAssemblyOptions = []
            for recursive_option in Option['RecursiveAssemblyOption']:
                subAssemblyOptions.append(self.setAssemblyOption(recursive_option))

            ASO.RecursiveAssemblyOption = subAssemblyOptions

            return ASO

        except:
            return []

    def json2object(self, jsonDescriptor):
        """
             Function to generate a AssemblySequence object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the AssemblySequence

        """

        # --interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)
            self.Name=jsonObject['Name']
            self.Description = jsonObject['Description']
            self.AssemblyMetric = [jsonObject['AssemblyMetric'][0],jsonObject['AssemblyMetric'][1]]

            # -- recursive AssemblyOptions --
            self.AssemblyOptions = self.setAssemblyOption(Option=jsonObject['AssemblyOptions'])




    def object2json(self):
        """
               Function to generate a json file from the AssemblySequence model
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class AssemblyOption():
    """
            AssemblyOption: Class representing the AssemblyOption

             :param string Name: Name of the AssemblyOption
             :param float Description: Cost of the AssemblyOption
             :param ObjectList Operations: OperationList of the AssemblyOption
             :param list OperatorMetric: OperatorMetric of the AssemblyOption
             :param ObjectList Operators: List of required operators of the AssemblyOption
             :param objectList ToolList: Required tools of the AssemblyOption
             :param objectList RecursiveAssemblyOption: Nested AssemblyOption

    """
    def __init__(self, JSONDescriptor=None, Name="", Description="",Operations=[],RecursiveAssemblyOption=[], DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.Operations = Operations
            self.RecursiveAssemblyOption = RecursiveAssemblyOption

        else:
            # TODO: import json descriptor to setup object
            x = 1

    def object2json(self):
        """
               Function to generate a json file from the AssemblySequence model
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class Operator():
    """
            Operator: Class representing the Operator

             :param string Name: Name of the Operator
             :param float CostPerHour: Cost of the Operator
             :param float Height: Height of the Operator in cm
             :param float MaxLiftingWeight: Maximum lifting capabilities of the Operator
             :param float Reach: Reach capabilities of the Operator

    """
    def __init__(self, JSONDescriptor=None, Name="", CostPerHour=70.0,Height=180.0,MaxLiftingWeight=50, Reach=155.0, DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.CostPerHour = CostPerHour
            self.Height = Height
            self.MaxLiftingWeight = MaxLiftingWeight
            self.Reach = Reach

        else:
            # TODO: import json descriptor to setup object
            x = 1

    def object2json(self):
        """
               Function to generate a json file from the AssemblySequence model
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class Tool():
    """
            Tool: Class representing the Tool   tool.hasName, tool.hasMass, tool.hasCost, tool.hasOrientation.hasData,
                                 tool.hasGeometry.hasDataInStepFile, requiredOperators

             :param string Name: Name of the Tool
             :param float Mass: Mass of the Tool
             :param float Cost: Cost of the Tool
             :param string Orientation: Orientation data of the Tool
             :param string hasGeometry: hasGeometry info of the Tool
             :param List RequiredOperators: List of required tool operators (referenced by name)

    """
    def __init__(self, JSONDescriptor=None, Name="", Mass=70.0,Cost=500.0,Orientation="",Geometry="", RequiredOperators=[], DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Mass = Mass
            self.Cost = Cost
            self.Orientation = Orientation
            self.Geometry = Geometry
            self.RequiredOperators = RequiredOperators

        else:
            # TODO: import json descriptor to setup object
            x = 1

    def object2json(self):
        """
               Function to generate a json file from the AssemblySequence model
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class Operation():       #
    """
        Product: Class representing the Operation

         :param string Name: Name of the Operation
         :param string Description: Description of the Operation
         :param list Fastner: Fastner identification
         :param list OperationMetric: Operation Metric identification
         :param list Operators: Operators identification
         :param list Tool: Tool identification
         :param objectList AssemblyOperationList: list of assemblyOperations
    """

    def __init__(self, JSONDescriptor=None, Name="", Description="", Fastners=[],OperationMetric=[],Operators = [], Tool=[], DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.Fastners = Fastners
            self.OperationMetric = OperationMetric
            self.Operators = Operators
            self.Tool = Tool


        else:
            self.json2object(JSONDescriptor)
            x = 10

    def json2object(self, jsonDescriptor):
        """
             Function to generate a Operation object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the Operation

        """

        # --interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)


    def object2json(self):
        """
               Function to generate a json file from the Operation model
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class Material():       #
    """
        Material: Class representing the material

         :param string Name: Name of the DomainVariable
         :param Double Density: Density of the material
         :param Double Cost: Cost of the material
         :param Double Damping: Damping of the material
         :param Double Transparency: Transparency of the material
         :param list Stiffness: Stiffness matrix of the material


    """

    def __init__(self, JSONDescriptor=None, Name="", Density=7.89,Cost=1.0, Damping=88.5,Transparency=90.0,Stiffness=[], DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Density = Density
            self.Cost = Cost
            self.Damping = Damping
            self.Transparency = Transparency
            self.Stiffness = Stiffness

        else:
            self.json2object(JSONDescriptor)
            x = 10

    def json2object(self, jsonDescriptor):
        """
             Function to generate a Material object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the Material

        """

        # --interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)


    def object2json(self):
        """
               Function to generate a json file from the Material model
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class Contact():       #
    """
        Contact: Class representing the contact

         :param string Name: Name of the Contact
         :param string Type: Density of the Contact
         :param Double SearchDistance: Search distance of the Contact
         :param list ApplicationAreas: list of application areas


    """

    def __init__(self, JSONDescriptor=None, Name="", Type="",SearchDistance=5.0,ApplicationAreas=[], DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Type = Type
            self.SearchDistance = SearchDistance
            self.ApplicationAreas = ApplicationAreas

        else:
            self.json2object(JSONDescriptor)
            x = 10

    def json2object(self, jsonDescriptor):
        """
             Function to generate a Contact object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the Contact

        """

        # --interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)


    def object2json(self):
        """
               Function to generate a json file from the Contact model
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class BoundaryCondition():       #
    """
        BoundaryCondition: Class representing the BoundaryCondition

         :param string Name: Name of the BoundaryCondition
         :param string Type: Density of the BoundaryCondition
         :param Double Value: Value of the BoundaryCondition
         :param list Direction: Direction vector of BoundaryCondition
         :param list DOF: DOF vector of BoundaryCondition
         :param list ApplicationAreas: list of application areas


    """

    def __init__(self, JSONDescriptor=None, Name="", Type="",Value=0.0,Direction=[],DOF=[],ApplicationAreas=[], DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Type = Type
            self.Value = Value
            self.DOF = DOF
            self.Direction = Direction
            self.ApplicationAreas = ApplicationAreas

        else:
            self.json2object(JSONDescriptor)
            x = 10

    def json2object(self, jsonDescriptor):
        """
             Function to generate a BoundaryCondition object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the Contact

        """

        # --interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)


    def object2json(self):
        """
               Function to generate a json file from the BoundaryCondition
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class ResultMetric():       #
    """
        ResultMetric: Class representing a result metric

         :param string Name: Name of the ResultMetric
         :param string Description: Description of the ResultMetric
         :param string Unit: Unit of the ResultMetric
         :param double Optimum: Optimum value of the ResultMetric
         :param double Value: Value of the ResultMetric


    """

    def __init__(self, JSONDescriptor=None, Name="", Description="",Optimum=5.0,Unit="",Value=0.0, DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.Optimum = Optimum
            self.Unit = Unit
            self.Value = Value

        else:
            self.json2object(JSONDescriptor)
            x = 10

    def json2object(self, jsonDescriptor):
        """
             Function to generate a Contact object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the Contact

        """

        # --interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)


    def object2json(self):
        """
               Function to generate a json file from the Contact model
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class AnalysisModel():       #
    """
        AnalysisModel: Class representing the AnalysisModel

         :param string Name: Name of the AnalysisModel
         :param string Description: Description of the AnalysisModel
         :param string GUID: Global unique identifier of the AnalysisModel
         :param string Version: Version of the AnalysisModel
         :param string ModelFile: ModelFile of the AnalysisModel
         :param string AnalysisType: AnalysisType of the AnalysisModel
         :param double SubsetNumber: SubsetNumber of the AnalysisModel
         :param list ModelDescription: ModelDescription of AnalysisModel [Formalism,Version,CreatedBy]
         :param list Mesh: MeshTypes of AnalysisModel [Meshtypes]
         :param object list Contacts: List of contacts of AnalysisModel
         :param object list BoundaryConditions: List of BoundaryConditions of AnalysisModel
         :param object list DecisionVariables: List of DecisionVariables of AnalysisModel
         :param list ApplicationAreas: list of application areas


    """

    def __init__(self, JSONDescriptor=None, Name="", Description="",Version="",GUID="",AnalysisType="",ModelFile="",SubsetNumber=0.0,ModelDescription=[],Mesh=[],Contacts=[],BoundaryConditions=[],DecisionVariables=[],ApplicationAreas=[], DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.GUID=GUID
            self.Version = Version

            self.ModelFile=ModelFile
            self.SubsetNumber=SubsetNumber
            self.ModelDescription=ModelDescription
            self.Mesh = Mesh
            #analysis elements
            self.AnalysisGUID = ""
            self.AnalysisType=AnalysisType
            self.ToolDescription = []
            self.AnalysisResults = []
            self.Responsepoints = []
            self.Contacts = Contacts
            self.BoundaryConditions = BoundaryConditions
            self.DecisionVariables = DecisionVariables
            self.ApplicationAreas = ApplicationAreas

        else:
            self.json2object(JSONDescriptor)
            x = 10

    def clean(self):
        self.ModelDescription = []
        self.Mesh = []
        self.Contacts = []
        self.BoundaryConditions = []
        self.DecisionVariables = []
        self.ApplicationAreas = []

    def json2object(self, jsonDescriptor):
        """
             Function to generate a BoundaryCondition object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the Contact

        """

        # --interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)


    def object2json(self):
        """
               Function to generate a json file from the BoundaryCondition
        """
        return json.dumps(self, default=lambda o: o.__dict__,indent=4)


#---------------------Ontology & contracts interface objects--------------------------

class Contract():       #
    """
        Contract: Class representing the Contract

         :param string Name: Name of the Contract
         :param string Description: Description of the Contract
         :param list Assmuptions: list of contract assumptions
         :param list Guarantees: list of contract guarantees
    """

    def __init__(self, JSONDescriptor=None, Name="", Description="", Assumptions=[],Guarantees=[], DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.Assumptions = Assumptions
            self.Guarantees = Guarantees


        else:
            self.json2object(JSONDescriptor)
            x = 10

    def json2object(self, jsonDescriptor):
        """
             Function to generate a Contract object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the Contract

        """

        # --interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)

            self.Name = jsonObject['Name']
            self.Description = jsonObject['Description']
            self.Assumptions = []
            for asmpt in jsonObject['Assumptions']:
                temp = []
                dv = DomainVariable(Name=asmpt[0]["Name"],Description=asmpt[0]["Description"],Unit=asmpt[0]["Unit"])
                temp.append(dv)
                temp.append(asmpt[1])
                temp.append(asmpt[2])
                self.Assumptions.append(temp)

            self.Guarantees = []
            for grnt in jsonObject['Guarantees']:
                temp = []
                dv = DomainVariable(Name=grnt[0]["Name"], Description=grnt[0]["Description"], Unit=grnt[0]["Unit"])
                temp.append(dv)
                temp.append(grnt[1])
                temp.append(grnt[2])
                self.Guarantees.append(temp)


    def object2json(self):
        """
               Function to generate a json file from the Contract model
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class Ontology():       #
    """
        Ontology: Class representing the Ontology

         :param string Name: Name of the Ontology
         :param string Description: Description of the Ontology
         :param objectlist Relations: list of relation objects
    """

    def __init__(self, JSONDescriptor=None, Name="", Description="", Relations=[], DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.Relations = Relations


        else:
            self.json2object(JSONDescriptor)
            x = 10

    def json2object(self, jsonDescriptor):
        """
             Function to generate a Ontology object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the Ontology

        """

        # --interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)

            self.Name = jsonObject['Name']
            self.Description = jsonObject['Description']
            self.Relations = []
            for relation in jsonObject['Relations']:
                temp = []
                source = DomainVariable(Name=relation['Source']['Name'],
                                        Description=relation['Source']['Description'],
                                        Unit=relation['Source']['Unit'])
                destination = DomainVariable(Name=relation['Destination']['Name'],
                                        Description=relation['Destination']['Description'],
                                        Unit=relation['Destination']['Unit'])
                r = Relation(Name=relation['Name'], Description=relation['Description'], Source=source,Destination=destination,SensitivityDirection=relation['SensitivityDirection'],Weight=relation['Weight'])
                self.Relations.append(r)


    def object2json(self):
        """
               Function to generate a json file from the Ontology model
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class Relation():       #
    """
        Relation: Class representing the Relation

         :param string Name: Name of the Relation
         :param string Description: Description of the Relation
         :param object Source: Source object of the relation.
         :param object Destination: Destination object of the relation
         :param string SensitivityDirection: SensitivityDirection of the relation (None = No directional sensitivity information)
         :param float Weight: Sensitivity weight of the relation (None = No sensitivity weight information)
    """

    def __init__(self, JSONDescriptor=None, Name="", Description="", Source = None,Destination = None,SensitivityDirection = None,Weight = 0.0, DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.Source = Source
            self.Destination = Destination
            self.SensitivityDirection = SensitivityDirection
            self.Weight = Weight


        else:
            self.json2object(JSONDescriptor)
            x = 10

    def json2object(self, jsonDescriptor):
        """
             Function to generate a Relation object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the Relation

        """

        # --interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)


    def object2json(self):
        """
               Function to generate a json file from the Relation model
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class DomainVariable():       #
    """
        DomainVariable: Class representing the DomainVariable

         :param string Name: Name of the DomainVariable
         :param string Description: Description of the DomainVariable
         :param string Unit: Unit of the DomainVariable
    """

    def __init__(self, JSONDescriptor=None, Name="", Description="", Unit="", DEBUG=True):
        self.DEBUG = DEBUG
        if JSONDescriptor is None:
            self.Name = Name
            self.Description = Description
            self.Unit = Unit


        else:
            self.json2object(JSONDescriptor)
            x = 10

    def json2object(self, jsonDescriptor):
        """
             Function to generate a DomainVariable object from a JSON file

             :param string jsonDescriptor: absolute path to the json file for the DomainVariable

        """

        # --interpret JSON file--
        with open(jsonDescriptor, "r") as read_file:
            jsonObject = json.load(read_file)


    def object2json(self):
        """
               Function to generate a json file from the DomainVariable model
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


