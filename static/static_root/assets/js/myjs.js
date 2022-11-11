$('#directorate_id').change(function(){
    let url = $('#department').attr('departments');
    let directorate= $(this).val()
    console.log(url)
    console.log(directorate)
    $.ajax({
        url:url,
        data:{'direct_id':directorate},
        success:(data)=>{
            $('#department_id').html(data)
            
        }

    })
})
$('#department_id').change(function(){
    let url = $('#department').attr('unit_urls');
    let department= $(this).val()
    $.ajax({
        url:url,
        data:{'dept_id':department},
        success:(data)=>{
            $('#unit_id').html(data)
            
        }

    })
})

$('#id_state_of_origin').change(function(){
    let url = $('#contact-form').attr('lgas-url');
    let state = $(this).val()
    $.ajax({
        url:url,
        data:{'state_id':state},
        success:(data)=>{
            $('#id_local_government_area').html(data)
            console.log(data)
        }

    })
})
$('#id_state_of_residence').change(function(){
    let url = $('#contact-form').attr('lgas-url');
    let state = $(this).val()
    $.ajax({
        url:url,
        data:{'state_id':state},
        success:(data)=>{
            $('#id_local_government_area_of_residence').html(data)
            console.log(data)
        }

    })
})
$('#id_state_of_permanent').change(function(){
    let url = $('#contact-form').attr('lgas-url');
    let state = $(this).val()
    $.ajax({
        url:url,
        data:{'state_id':state},
        success:(data)=>{
            $('#id_local_government_area_of_permanent').html(data)
            console.log(data)
        }

    })
})
