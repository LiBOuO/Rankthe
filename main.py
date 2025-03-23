from src.factory import FileControllerFactory

fileController = FileControllerFactory.get_controller("local")
fileController.createCSV(["a", "b", "c"])
fileController.addRowAndReturnResult(["1", "2", "3"])
print(fileController.getFile())