import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager

class QuestLogRequest(GenericRequest):
    """
    Get info from the quest log about which quests are completed and which stage of each uncompleted quest the player is on
    """

    def __init__(self, session, page):
        super(QuestLogRequest, self).__init__(session)

        # page=1 for current quests
        # page=2 for completed quests
        self.url = session.serverURL + "questlog.php?which=" + str(page)

    def parseResponse(self):

        self.responseData["text"] = self.responseText

        questTitlePattern = PatternManager.getOrCompilePattern("questsCompleted")
        questOrePattern = PatternManager.getOrCompilePattern("oreType")

        # make a map from quest names to quest descriptions
        quests = {}
        for match in questTitlePattern.finditer(self.responseText):
            quest = {}
            quest['status'] = match.group(2)

            # for the Mt. McLargeHuge quest
            oreMatch = questOrePattern.search(match.group(2))
            if oreMatch != None:
                quest['oreType'] = oreMatch.group(1)
            quests[match.group(1)] = quest
 
        self.responseData["quests"] = quests
