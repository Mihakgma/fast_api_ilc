from pandas import DataFrame
from fastapi import UploadFile
from pydantic import BaseModel, Field, model_validator

from app.funct.df_functions import excel_to_data_frame_parser


class UploadExcelFile(BaseModel):
    excel_file: UploadFile = Field(..., description="Excel file to upload")
    df: DataFrame = None
    df_info: dict = None

    @model_validator(mode='after')
    def _set_df_info(self):
        if self.df is not None:
            self.df = excel_to_data_frame_parser(self.excel_file.filename)
            self.df_info = self._create_df_info(self.df)
        return self

    def _create_df_info(self, df: DataFrame) -> dict:
        return {
            'shape': df.shape,
            'dtypes': df.dtypes.to_dict(),
            'description': df.describe().to_dict(),
            'columns': list(df.columns),
            'data': df.to_dict(orient='records')  # <-- Serialize to list of dictionaries
        }
