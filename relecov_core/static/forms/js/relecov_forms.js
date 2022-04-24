function summaryBin(evt, selected_option) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(selected_option).style.display = "block";
    evt.currentTarget.className += " active";
}

function setJExcelTable(){
    var data = [[],[],[],[],[],[]];//initialized with 6 empty rows
    var mySpreadsheet = jspreadsheet(document.getElementById('spreadsheet'), {
    data:data,
    csvHeaders:true,
    tableOverflow:true,
    columns: [
        { type: 'text', title:'Public Health sample id (SIVIES)', width:230 },
        { type: 'text', title:'Sample ID given by originating laboratory', width:280 },
        { type: 'text', title:'Sample ID given by the submitting laboratory', width:300 },
        { type: 'text', title:'Sample ID given in the microbiology lab', width:280 },
        { type: 'text', title:'Sample ID given if multiple rna-extraction or passages', width:280 },
        { type: 'text', title:'Sample ID given for sequencing', width:280 },
        { type: 'text', title:'Sample ID given by originating laboratory', width:280 },
        { type: 'text', title:'Sample ID given by the submitting laboratory', width:280 },
        { type: 'text', title:'Sample ID given in the microbiology lab', width:280 },
        { type: 'text', title:'Sample ID given if multiple rna-extraction or passages', width:280 },
        { type: 'dropdown', title:'Originating Laboratory', width:280, source:[ 
        "Hospital Clínic de Barcelona (HCB)", "Instituto de Salud Carlos III ", "Microbiología HUC San Cecilio, Granada ",
        "Microbiología. Hospital Universitario Virgen del Rocio. Sevillia", "Hospital Clínico Universitario Lozano Blesa", "Hospital Universitario Miguel Servet",
        "Centro de Investigación Biomédica de Aragón", "Hospital Universitario Central de Asturias", "Servicio de Microbiologia HU Son Espases", 
        "Hospital Universitario Ntra. Sra de Candelaria (HUNSC)", "Instituto Tecnológico y de Energías Renovables, S.A. (ITER) - centro de referencia",
        ] },
        { type: 'text', title:'Sample Collection Date', width:280 },
        { type: 'text', title:'Sample Received Date', width:280 },
        { type: 'dropdown', title:'Specimen source', width:280, source:[ 
        "Nasopharynx aspirate", "Oral epithelium from ectoderm biopsy", "Skin epidermis biopsy",
        "Epithelium biopsy", "Bronchial lymph node biopsy", "Hepatic diverticulum biopsy",
        "Liver bud biopsy", "Biliary bud biopsy", "Gall bladder biopsy", 
        "Liver biopsy", "Lung biopsy","Oropharynx biopsy","Nasopharynx biopsy","Respiratory tract biopsy",
        ] },
        { type: 'dropdown', title:'Environmental Material', width:280, source:[ 
        "Animal litter", "Animal manure", "Farmyard manure",
        "Fresh animal manure", "Horse manure", "Pig manure",
        "Stable manure", "Anthropogenic environmental material", "Agricultural environmental material", 
        "Food material", "Food isolate","Food source","Algae","Animal",
        ] },
        { type: 'text', title:'Host Age', width:280 },
        { type: 'text', title:'Host Gender', width:280 },
        { type: 'text', title:'Sequence file R1 fastq', width:280 },
        { type: 'text', title:'Sequence file R2 fastq', width:280 },
    ],

    allowInsertColumn:false,
    allowDeleteColumn:false,
    allowRenameColumn:false,
    csvFileName:'samples',
    //minDimensions:[{{sample_information.table_size}},3],
    });

    document.getElementById('download').onclick = function () {
    mySpreadsheet.download();
    }
}