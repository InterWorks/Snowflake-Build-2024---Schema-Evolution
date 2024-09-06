
# Define set of utility functions leveraged by the notebooks

## Imports
import streamlit as st
import re
import math

## Define function to print the set of shareable QR codes
def print_qr_codes():
  qr_col_1, qr_col_2, qr_col_3 = st.columns(3, gap="large")
  with qr_col_1:
    st.subheader("View this repository")
    st.image("images/QR-repo.png", caption="This repository")
    st.markdown("[https://github.com/InterWorks/Snowflake-Build-2024---Schema-Evolution](https://github.com/InterWorks/Snowflake-Build-2024---Schema-Evolution)")
  with qr_col_2:
    st.subheader("View my company profile")
    st.image("images/QR-IW-profile.png", caption="My company profile")
    st.markdown("[https://interworks.com/people/chris-hastie](https://interworks.com/people/chris-hastie)")
  with qr_col_3:
    st.subheader("View my LinkedIn profile")
    st.image("images/QR-LinkedIn.png", caption="My LinkedIn profile")
    st.markdown("[https://www.linkedin.com/in/chris-hastie/](https://www.linkedin.com/in/chris-hastie/)")

## Define function that returns all the code templates leveraged in the notebooks
def retrieve_code_templates():

  ### Define code, using extra indenting for readability at this stage
  code_templates_raw = [
      {
          "name": "Infer schema"
        , "code_template": """
              table(
                infer_schema(
                    location => '<location of file(s), including stage>'
                  , file_format => '<Snowflake File Format object to use when reading the file>'
                )
              )
            """
      }
    , {
          "name": "Table template"
        , "code_template": """
              select array_agg(object_construct(*))
              table(
                infer_schema(
                    location => '<location of file(s), including stage>'
                  , file_format => '<Snowflake File Format object to use when reading the file>'
                )
              )
            """
      }
    , {
          "name": "Create table"
        , "code_template": """
              create or replace table "MY_TABLE"
              using template(
                select array_agg(object_construct(*))
                from table(
                  infer_schema(
                      location => '<location of file(s), including stage>'
                    , file_format => '<Snowflake File Format object to use when reading the file>'
                  )
                )
              )
              comment = 'Table created using the metadata inferred from the source file(s)'
            """
      }
    , {
          "name": "Ingest data"
        , "code_template": """
              copy into "MY_TABLE"
              from '@<location of file(s), including stage>'
                file_format = "<Snowflake File Format object to use when reading the file>"
                match_by_column_name = CASE_INSENSITIVE
            """
      }
    , {
          "name": "Create table with schema evolution"
        , "code_template": """
              create or replace table "DATA_FROM_ALL_SOURCES"(
                  "METADATA_FILE_PATH"                    string          comment 'Full path for the file in the originating stage'
                , "METADATA_FILE_ROW_NUMBER"              integer         comment 'Row number within the file in the originating stage'
                , "METADATA_RECORD_INGESTION_TIMESTAMP"   timestamp_ltz   comment 'Timestamp of record ingestion in local timezone'
              )
                enable_schema_evolution = TRUE
                comment = 'Table containing data from all sources, with schema evolution enabled to automatically add new columns as required'
            """
      }
    , {
          "name": "Ingest data with metadata fields"
        , "code_template": """
              copy into "MY_TABLE"
              from '<location of file(s), including stage>'
                file_format = "<Snowflake File Format object to use when reading the file>"
                match_by_column_name = CASE_INSENSITIVE
                include_metadata = (
                    "METADATA_FILE_PATH" = METADATA$FILENAME
                  , "METADATA_FILE_ROW_NUMBER" = METADATA$FILE_ROW_NUMBER
                  , "METADATA_RECORD_INGESTION_TIMESTAMP" = METADATA$START_SCAN_TIME
                )
            """
      }
  ]

  ### Clean up the code by removing all the extra indenting
  code_templates = [
    {
        "name": x["name"]
      , "code_template": x["code_template"].replace(re.search("\n(\s+)[^\s].*", x["code_template"]).group(1), "")
    }
    for x in code_templates_raw
  ]

  return code_templates

## Define function to print all of the code templates in different columns
def print_code_templates(column_count: int = 2):
  code_templates = retrieve_code_templates()

  ### Split the number of values in the code_templates
  ### list into an appropriate number of rows
  row_count = math.ceil(len(code_templates) / column_count)

  ### Iterate over each row to create a set of columns
  for row in range(row_count):
    cols = st.columns(column_count)

    ### Iterate over each column for the row
    ### and output the code template information
    for i, col_x in enumerate(cols):
      with col_x:
        member_index = (column_count * row) + i
        if member_index < len(code_templates):
          st.write(code_templates[member_index]["name"])
          st.code(code_templates[member_index]["code_template"], "sql")
