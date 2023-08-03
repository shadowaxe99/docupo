from backend.document_parser import parseDocument

class RepositoryGenerator:
    def __init__(self):
        self.repo_structure = {}

    def generateRepoStructure(self, document):
        parsed_content = parseDocument(document)
        self.repo_structure = self._buildStructure(parsed_content)
        return self.repo_structure

    def _buildStructure(self, parsed_content):
        structure = {}
        for section in parsed_content:
            structure[section['title']] = section['content']
        return structure

    def reviewRepoStructure(self):
        return self.repo_structure

    def modifyRepoStructure(self, modifications):
        self.repo_structure.update(modifications)
        return self.repo_structure
```