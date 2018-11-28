$('document').ready(function(){
    /*For mobile version of left side bar*/
    $(".button-collapse").sideNav();
    /*For dropdown*/
    $('select').material_select();
    
    /*Registration form validation*/
    // $("#reg_form").validate({
    //     rules: {
    //         first_name: {
    //             required: true
    //         },
    //         last_name: {
    //             required: true
    //         },
    //         username: {
    //             required: true
    //         },
    //         pass: {
    //             required: true,
    //             minlength: 6
    //         },
    //         confirm_password: {
    //             required: true,
    //             equalTo: "#password"
    //         },
    //         userStatus: {
    //             required: true
    //         }
    //     },
    //     messages: {
    //         first_name:{
    //             required: ""
    //         },
    //         last_name:{
    //             required: ""
    //         },
    //         username: {
    //             required: ""
    //         },
    //         pass: {
    //             required: "",
    //             minlength: "Не менее 6 символов"
    //         },
    //         confirm_password: {
    //             required: "Заполните все поля",
    //             equalTo: "Пароли должны совпадать"
    //         },
    //         userStatus: {
    //             required: "Выберите из списка*"
    //         }
    //     },
    //     errorElement: "span",
    //     errorClass: "invalid"
    // });
    // /*Authorization form validation*/
    // $('#authForm').validate({
    //     rules: {
    //         login: {
    //             required: true
    //         },
    //         authPassword: {
    //             required: true,
    //             minlength: 6
    //         }
    //     },
    //     messages: {
    //         login: {
    //             required: "Заполните поле"
    //         },
    //         authPassword: {
    //             required: "Заполните поле",
    //             minlength: "Не менее 6 символов"
    //         }
    //     },
    //     errorElement: "span",
    //     errorClass: "invalid"
    // });
});
// window.onload = function(){
//     $('#reg_form')[0].reset();
// };

// var respTableDiv = $('<div>', { "class": "table-responsive"}).appendTo('#test1');



/*Show password button*/
$('#showPassword').click(function(){
  if ($('#password').prop('type') == 'password' && $('#confirm_password').prop('type') == 'password') {
    $('#password').prop('type', 'text');
    $('#confirm_password').prop('type', 'text');
} else {
    $('#password').prop('type', 'password');
    $('#confirm_password').prop('type', 'password');
}
});
