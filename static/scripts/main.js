// $(document).on('submit', '#post-form', function(e){
//     e.preventDefault();
//     lat1 = $('#lat1').val()
//     lon1 = $('#lon1').val()

//     $ajax({
//         type: 'POST',
//         url: '{% url "distance_ajax" %}',
//         data: {
//             'latitude': lat1,
//             'longitude': lon1
            
//         },
//         success: function(response){
//             console.log(response)
//             data = response.nearby_distance
//             for(i=0; i<data.length; i++){
//                 $('#data_table tbody').append(
//                     `
//                     <tr>
//                         <td>${data[i]}</td>
//                     </tr>
//                     `
//                     )
//             }
//         }
//     })

})