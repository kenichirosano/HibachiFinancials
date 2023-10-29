Flow of program 1 - preparation

Create SQL tables for 
1. Edinet code
2. Document Set

Flow of program 2 - main
Create documentSet_id
Get 
1. Unit
2. Context
3. DTS (Discoverable Taxonomy Set)
4. Roletype
5. Linkbase
6. RoleRef
7. Concept
8. Instance
9. FootNote

Taxonomy is defined in XML Schema (Taxonomy Schema) with linkbases.
Concept is defined with name and data type.
Linkbases defines relationships between concepts (inter-concept relationships) or between concepts and documents.
Linkbase is a collection of the 5 extended links: definition, calculation, presentation, label and reference.
