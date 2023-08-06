function Collapse(product){
    const element_btn = "btn" + product;
    const element_collapse = product + "-collapse";
    if (["Teachers", "Classes"].includes(product)) {
      document.getElementById(element_btn).className = "btn-toggle align-items-center rounded list-group-level2";
    } else {
      document.getElementById(element_btn).className = "btn-toggle align-items-center rounded";
    }
    document.getElementById(element_btn).setAttribute('aria-expanded', 'true');
    document.getElementById(element_collapse).className = "collapse show";
}


function ShowNewOption(product, url){
    document.getElementById('btn-new').removeAttribute("hidden");
    document.getElementById('btn-new').classList.remove('disabled');
    var a = document.getElementById('btn-new');
        a.href = url;
        a.textContent = product;
}

function ShowNewFamOption(product, url){
    document.getElementById('btn-new-fam').removeAttribute("hidden");
    document.getElementById('btn-new-fam').classList.remove('disabled');
    var a = document.getElementById('btn-new-fam');
        a.href = url;
        a.textContent = product;
}

function ShowEditOption(product, url){
    const el_showEditBTN = "btnEdit" + product;
    const array1 = [el_showEditBTN, 'btn-edit'];
    for (const element of array1) {
        // ...use `element`...
        document.getElementById(element).removeAttribute("hidden");
        document.getElementById(element).classList.remove('disabled');
        var a = document.getElementById(element);
            a.href = url;
    }
}

function ShowDeleteOption(product, deleteID){
    const el_showDeleteBTN = "btnDelete" + product;
    const array1 = [el_showDeleteBTN, 'btn-delete'];
    for (const element of array1) {
        document.getElementById(element).removeAttribute("hidden");
        document.getElementById(element).classList.remove('disabled');
        var b = document.getElementById(element);
            b.dataset.target = "#exampleModalCenter" + deleteID;
            b.dataset.toggle = "modal";
    }
}

function setCurrentValue(element, url){
    var e = document.getElementById(element);
        e.value = url;
}
