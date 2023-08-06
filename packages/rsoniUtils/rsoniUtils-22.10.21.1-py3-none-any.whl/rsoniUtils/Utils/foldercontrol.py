import os
import sys

FOLDER_PREFIX = "C:\\Users\\rslocal\\OneDrive\\rsdevvm.StockAnalysis\\"

##########################################################


class clsFolderControl:
    def __init__(self, folderPrefix):
        self.Name = "folder_control"
        self.FolderPrefix = folderPrefix

    def CheckEmptyFolder(self, deleteFolder=False):
        folderPath = self.FolderPrefix+"data\\"
        totalDirCount = 0
        totalDeletingDirCount = 0
        if (os.path.exists(folderPath) == True):
            print("Folder Exists")
            for dirr in os.scandir(folderPath):
                if (dirr.is_dir()):
                    totalDirCount = totalDirCount+1
                    TotalSize = os.path.getsize(dirr.path)
                    #print(dirr.name, " Size ", TotalSize)
                    if (TotalSize <= 0):
                        totalDeletingDirCount = totalDeletingDirCount+1
                        print("Deleting:", dirr.name, " Size ", TotalSize)
                        try:
                            os.rmdir(dirr.path)
                        except OSError as error:
                            print("Dir can not be removed", str(error))
                        # break
            print("TotalDir:", totalDirCount,
                  "TotalDeletingDir:", totalDeletingDirCount)
        else:
            print("Folder doesn't Exists")
###########################################################


#ObjfolderControl = clsFolderControl()
# ObjfolderControl.CheckEmptyFolder()
