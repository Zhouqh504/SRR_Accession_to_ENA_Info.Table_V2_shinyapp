#the script was created by zhouqh 2023.5.17
import requests
import pandas as pd
from shiny import ui, render, App
import io
import time
from datetime import date



#df = pd.read_table(r"D:\帮忙搞完删\ena.txt")
# Create an empty DataFrame to store the results
results_df = pd.DataFrame()

app_ui = ui.page_fluid(

    ui.h2("SRR Accession to ENA Info. Table V2"),
    ui.markdown("""
        This app is modified from TBtools function "SRRnum to ENA info. Table" for obtaining ENA links information based on SRR numbers. NCBI only stores parts of SRR data in .sra format. DDBJ stroes less, while it contains most data in .sra format with a few in .fastq format. ENA database is the best one, which stores almost all short read sequencing data in SRA and Fastq format. To get the links requires some coding jobs. Thus, this function is developed. It takes a list of SRR numbers and return info. in ENA database.To each SRR num, it would take about 3 seconds, so if the list is too long, for example, 100 SRRnums, it would take almost 300 seconds, that is 5 minutes.
    Enjoy it!   
    """),
    #ui.input_file("SRRnum","SRR number(s) Input"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_file("file1", "Choose SRRnum CSV File", accept=[".csv"], multiple=False),
            #ui.input_checkbox("header", "Header", True),
            ui.download_button("downloadData", "Download"),
        ),
        #ui.panel_main(ui.output_ui("contents")),

    #ui.input_text_area("SRRnum", "SRR number(s) Input", placeholder="Enter accession",value="SRR9331505"),
    #ui.output_ui("contents"),
    ui.panel_main(ui.output_ui("contents")),
)
)
def server(input, output, session):
    @output
    @render.ui
    def contents():
        if input.file1() is None:
            return "Please upload a CSV file"

        file_info: list[FileInfo] = input.file1()
        file_path = file_info[0]["datapath"]
        df = pd.read_csv(file_path, header=None)
        results_df = pd.DataFrame()

        for index, row in df.iterrows():
            accession = row[0]
            url = f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={accession}&result=read_run&fields=study_accession,sample_accession,secondary_sample_accession,experiment_accession,run_accession,tax_id,scientific_name,instrument_model,library_layout,fastq_ftp,fastq_galaxy,submitted_ftp,submitted_galaxy,sra_ftp,sra_galaxy,sra_aspera,fastq_aspera"

            response = requests.get(url)
            response.raise_for_status()

            # Convert the response content to a DataFrame
            data = pd.read_csv(io.StringIO(response.content.decode('utf-8')), delimiter='\t')

            # Append the data to the results DataFrame
            results_df = pd.concat([results_df, data], ignore_index=True)


            print(f"Download finish Accession: {accession}")

            time.sleep(3)
        #return results_df
        #return ui.HTML(results_df.to_html(classes="table table-striped"))

        @session.download(
            filename=lambda: f"results_df-{date.today().isoformat()}.csv"
        )
        async def downloadData():
            csv_data = results_df.to_csv(index=False)
            yield csv_data

        download_link = ui.download_link("Download", downloadData)
        return ui.panel_main([

            ui.HTML(results_df.to_html(classes="table table-striped")),
            download_link
        ])

    return contents






app = App(app_ui, server)

