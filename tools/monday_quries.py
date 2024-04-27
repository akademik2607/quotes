from graphql_query import Argument, Query, Field, Operation, Fragment, InlineFragment
import requests


# query GetBoardItems{
#       items (ids: [1470349673]){
#         id
#         name
#         column_values {
#           column {
#             id
#             title
#           }
#           text
#           id
#           value
#         }
#       }
# }

class MondayEngine:
    def __init__(self):
        self.token = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjM1MjgyMTI2OSwiYWFpIjoxMSwidWlkIjo1OTQwOTU1MCwiaWFkIjoiMjAyNC0wNC0yN1QwODoxNTo1NC42MDRaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTc5NDIxMTksInJnbiI6ImV1YzEifQ.onqegk-dUqt3O92NldMcRwzuuF_HjKGI6DX_I7ToQz4'
        self.api_url = 'https://api.monday.com/v2'
        self.headers = {"Authorization": self.token, "API-Version": "2023-04"}
        self.query_data = ''
        self.row_data = ''
        self.data = ''


    def get_monday_quote_columns_values(self, item_id):
        self._get_monday_quote_columns_values(item_id)
        data = self._get_query().json()
        result = {}
        for item in data.get('data').get('items'):
            print(item.get('name'))
            result['name'] = item.get('name', None)
            for column_value in item.get('column_values'):
                if column_value.get('id') == 'dropdown':
                    result['currency'] = column_value.get('text', None)
                if column_value.get('id') == 'numbers32':
                    result['quotation_num'] = column_value.get('text', 0)
                if column_value.get('id') == 'mirror61':
                    result['quotation_ref'] = column_value.get('display_value', 0)
                if column_value.get('id') == 'item_id2':
                    result['item_id'] = column_value.get('text', None)
                if column_value.get('id') == 'mirror38':
                    result['origin'] = column_value.get('display_value', '')
                if column_value.get('id') == 'mirror63':
                    result['origin_city'] = column_value.get('display_value')
                if column_value.get('id') == 'mirror5':
                    result['service_typ'] = column_value.get('display_value')
                if column_value.get('id') == 'mirror50':
                    result['method'] = column_value.get('display_value')
                if column_value.get('id') == 'mirror6':
                    result['volume'] = column_value.get('display_value')
                if column_value.get('id') == 'mirror4':
                    result['destination'] = column_value.get('display_value')
                if column_value.get('id') == 'mirror69':
                    result['freight_mode'] = column_value.get('display_value')
                if column_value.get('id') == 'mirror49':
                    result['transit_time'] = column_value.get('display_value')
                if column_value.get('id') == 'mirror19':
                    result['weight_up_to'] = column_value.get('display_value')

                # print(column_value)
            # print(result)
        return result
                # weight_up_to = data.get('weight_up_to', 'TestWeightUpTo')


    def _get_monday_quote_columns_values(self, item_id):
        items_ids = Argument(name="ids", value=[item_id])

        mirrorFields = Fragment(
            name="MirrorFields",
            type="MirrorValue",
            fields=['column', 'id']
        )

        item_info = Query(
            name='items',
            arguments=[items_ids],
            fields=[
                'id',
                'name',
                Field(
                    name='column_values',
                    fields=[
                        'id',
                        'text',
                        InlineFragment(type="MirrorValue", fields=['display_value', 'id']),
                    ]
                )
            ])
        operation = Operation(type='query', queries=[item_info])
        print(operation.render())
        self.query_data = operation.render()

    def _get_query(self):
        self.data = {'query': self.query_data}
        return requests.post(url=self.api_url, json=self.data, headers=self.headers)


if __name__ == '__main__':
    MondayEngine().get_monday_quote_columns_values(1470349673)
