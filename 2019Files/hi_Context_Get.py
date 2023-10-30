# -*- coding: utf-8 -*-

def getContext(root_ElementTree):

    # To hold content's elements and attributes
    list_of_Contexts = []
    for context_ElementTree in root_ElementTree.findall('context'): # Find <context> element
        dict_of_Context = {
            'id':None
            ,'edinetCode':None
            ,'identifier':None
            ,'instant':None
            ,'forever':None
            ,'startDate':None
            ,'endDate':None
            ,'segment':None
            ,'scenario':None
            ,'dimension':None
            ,'member':None
        }
        dict_of_Context['id'] = context_ElementTree.get('id')

        for period_ElementTree in context_ElementTree.findall('period'):

            for startDate_ElementTree in period_ElementTree.findall('startDate'):
                dict_of_Context['startDate'] = startDate_ElementTree.text

            for endDate_ElementTree in period_ElementTree.findall('endDate'):
                dict_of_Context['endDate']   = endDate_ElementTree.text

            for instant_ElementTree in period_ElementTree.findall('instant'):
                dict_of_Context['instant']   = instant_ElementTree.text

            for forever_ElementTree in period_ElementTree.findall('forever'):
                dict_of_Context['forever']   = 'True'

        for entityElement in context_ElementTree.findall('entity'):

            for identifier_ElementTree in entityElement.findall('identifier'):
                dict_of_Context['edinetCode'] = identifier_ElementTree.text.split("-")[0] # [Edinet code]-[追番]
                dict_of_Context['identifier'] = identifier_ElementTree.text # [Edinet code]-[追番]

        for scenario_ElementTree in context_ElementTree.findall('scenario'):
            dict_of_Context['scenario'] = True

            for dimension_ElementTree in scenario_ElementTree.findall('explicitMember'):
                dict_of_Context['dimension'] = dimension_ElementTree.get('dimension')
                dict_of_Context['member']    = dimension_ElementTree.text

        list_of_Contexts.append(dict_of_Context)

    return list_of_Contexts
'''
4.7.1 The @id attribute
Every <context> element MUST include the @id attribute.
The @id attribute identifies the context (see Section 4.7) so that it may be referenced by item elements.
'''

'''
「報告書インスタンス作成ガイドライン」 2012 年（平成 24 年）3 月 14 日

p.14 6．コンテキストの定義
コンテキストに設定する内容は、id 属性、エンティティ(entity)要素、期間時点(period)要素、シナリオ(scenario)要素です。

p.19 6-3 エンティティ要素の設定
識別子(identifier)  {EDINET コード}-{追番}

p.21 6-5 シナリオ要素の設定
企業別タクソノミにおいて、個別財務諸表と連結財務諸表の両方で用いられている勘定科目(要素)は、同じ要素で定義されています。
したがって、報告書インスタンスにおいて報告する値が個別財務諸表のものか連結財務諸表のものかはコンテキストで区別されます。
シナリオ要素の設定がない場合、連結と判断します。

p.39
11-1 コンテキスト ID
'''
