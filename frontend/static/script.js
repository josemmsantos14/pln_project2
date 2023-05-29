function deleteTerm(designation){
    $.ajax("/term/" + designation, {
        type: "DELETE"
    })
    location.reload()
    
}
