from database import connect_to_db

account_query = "select * from KNA1 a left join KNB1 b on a.KUNNR = b.KUNNR and b.BUKRS = 1101 left join KNVV c on a.KUNNR = c.KUNNR and c.VKORG = 1101"


TABLE_REFERENCE = {
    "sales_district": {"table": "T171", "view": "T171_SF", "where": None},
    "sales_group": {"table": "TVKGR", "view": "TVKGR_SF", "where": None},
    "plant": {"table": "T001W", "view": "T001W_SF", "where": "VKORG = '1101'"},
    "stock": {"table": "MARD", "view": "MARD_SF", "where": "WERKS like 3*, 9*"},
    "sales_office": {"table": "TVKBT", "view": "TVKBT_SF", "where": None},
    "region": {"table": "T005S", "view": "T005S_SF", "where": None},
    "product_master_1": {
        "table": "MARA",
        "view": "MARA_SF",
        "where": 'MTART = "ZERT", "HAWA"',
    },
    "product_master_2": {"table": "MAKT", "view": "MAKT_SF", "where": None},
    "product_master_3": {"table": "MARC", "view": "", "where": "WERKS like 3*, 9*"},
    "customer_master_1": {"table": "KNA1", "view": "KNA1_SF", "where": None},
    "customer_master_2": {"table": "KNB1", "view": "KNB1_SF", "where": 'BUKRS ="1101"'},
    "customer_master_3": {
        "table": "KNVV",
        "view": "KNVV_SF",
        "where": 'VKORG = "1101"',
    },
    "changes": {"table": "CDHDR", "view": "CDHDR_SF", "where": 'TCODE ="XD02", "MM02"'},
    "billing": {
        "table": "VBRK",
        "view": "VBRK_SF",
        "where": 'VKORG = "1101" and FKDAT >= "01.04.2022"',
    },
    "billing_item": {"table": "VBRP", "view": "VBRP_SF", "where": None},
    "customer_cr_information": {
        "table": "KNKK",
        "view": "KNKK_SF",
        "where": 'KKBER ="1101"',
    },
    "employee_master": {
        "table": "PA0001",
        "view": "PA0001_SF",
        "where": 'BUKRS ="1101"',
    },
    "product_value": {"table": "A304", "view": "A304_SF", "where": 'VKORG = "1101"'},
    "discount_2_2": {"table": "A938", "view": "A938_SF", "where": 'VKORG = "1101"'},
    "discount_2_1": {"table": "A966", "view": "A966_SF", "where": 'VKORG = "1101"'},
    "discount_3": {"table": "A911", "view": "A911_SF", "where": 'VKORG = "1101"'},
    "discount_1": {"table": "A005", "view": "A005_SF", "where": 'VKORG = "1101"'},
    "gst_info_1": {"table": "A770", "view": "A770_SF", "where": None},
    "gst_info_2": {"table": "A771", "view": "A771_SF", "where": None},
    "gst_info_3": {"table": "A769", "view": "A769_SF", "where": None},
    "pricing_discount_gst": {"table": "KONP", "view": "KONP_SF"},
    "customer_outstanding_1": {
        "table": "BSID",
        "view": "BSID_SF",
        "where": 'BUKRS ="1101"',
    },
    "customer_outstanding_2": {
        "table": "BSAD",
        "view": "BSAD_SF",
        "where": 'BUKRS ="1101"',
    },
    "customer_outstanding_3": {
        "table": "KNC1",
        "view": "KNC1_SF",
        "where": 'BUKRS ="1101"',
    },
}

# def get_column_alias_mapping(query):
#     # Extract columns and their aliases from the query
#     column_alias_mapping = {}
#     select_part = query.lower().split("from")[0].replace("select", "").strip()
#     for col_alias in select_part.split(","):
#         col, alias = [part.strip() for part in col_alias.split(" as ")]
#         if '.' in alias:
#             alias = alias.split('.')[-1]
#         column_alias_mapping[col] = alias
#     return column_alias_mapping


async def get_column_alias_mapping_1(query):
    # Extract columns and their aliases from the query
    column_alias_mapping = {}
    alias_count = {}

    select_part = query.split("from")[0].replace("SELECT", "").strip()
    for col_alias in select_part.split(","):
        col_alias = col_alias.strip()

        # Split column and alias
        if " AS " in col_alias.upper():
            alias, col = [part.strip() for part in col_alias.split(" AS ")]
            if "." in alias:
                alias = alias.split(".")[-1]

        else:
            col = col_alias
            alias = col
        # Ensure unique aliases
        original_alias = alias
        count = alias_count.get(original_alias, 0)
        while alias in column_alias_mapping.keys():
            count += 1
            alias = f"{original_alias}_{count}"
        alias_count[original_alias] = count

        # Map the fully qualified column name to the unique alias
        column_alias_mapping[alias] = col

    return column_alias_mapping

async def get_unique_columns(cursor_description):
    columns = [column[0] for column in cursor_description]
    unique_columns = []
    column_count = {}

    for col in columns:
        if col in column_count:
            column_count[col] += 1
            unique_col = f"{col}_{column_count[col]}"
        else:
            column_count[col] = 0
            unique_col = col

        unique_columns.append(unique_col)

    return unique_columns

def get_column_alias_mapping(query):
    # Extract columns and their aliases from the query
    column_alias_mapping = {}
    alias_count = {}

    select_part = query.lower().split("from")[0].replace("select", "").strip()
    for col_alias in select_part.split(","):
        col_alias = col_alias.strip()

        # Split column and alias
        if " as " in col_alias:
            col, alias = [part.strip() for part in col_alias.split(" as ")]
            if "." in col:
                col = col.split(".")[-1]
        else:
            col = col_alias
            alias = col_alias.split(".")[-1]  # Default alias is the column name itself

        # Ensure unique aliases
        original_alias = alias
        count = alias_count.get(alias, 0)
        while alias in column_alias_mapping.values():
            print(alias_count)
            count += 1
            alias = f"{original_alias}_{count}"
            # print("alias", alias)
        alias_count[original_alias] = count

        column_alias_mapping[alias] = col

    return column_alias_mapping


def execute_dynamic_query(table_name, dynamic_where=None, page_number=1, page_size=10):
    conn = connect_to_db()
    if conn:
        try:
            # Execute queries or perform database operations
            cursor = conn.cursor()
            # Construct the SQL query without the WHERE clause if dynamic_where is None
            if dynamic_where is None:
                query = f"SELECT * FROM {table_name}_SF ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
                cursor.execute(query, ((page_number - 1) * page_size, page_size))
            else:
                # Construct the SQL query with the WHERE clause
                offset = (page_number - 1) * page_size
                query = f"SELECT * FROM {table_name}_SF WHERE {dynamic_where} ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
                cursor.execute(query, (offset, page_size))

            rows = cursor.fetchall()
            # Extract column names
            columns = [column[0] for column in cursor.description]

            result = [
                {column: value for column, value in zip(columns, row)} for row in rows
            ]

            cursor.close()
            conn.close()
            return {"data": result}
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "Failed to establish database connection"}
