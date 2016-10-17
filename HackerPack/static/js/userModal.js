    function showRegisterForm(){
    $('.loginBox').fadeOut('fast',function(){
        $('.forgotBox').fadeOut('fast');
        $('.registerBox').fadeIn('fast');
        $('.button-facebook').fadeIn('fast');
        $('.division').fadeIn('fast');
        $('.login-footer').fadeOut('fast',function(){
            $('.register-footer').fadeIn('fast');
        });
        $('.modal-title').html('Join the community and interact with all HackMates!');
        $('.button-facebook').html('Sign Up with Facebook');
        $('.tooltip-test').show();
        $('.tooltip-test').tooltip();
        $(".signupform").collapse('hide');
    });
    $('.error').removeClass('alert alert-danger').html('');
    }

    function showLoginForm(){
        $('.registerBox').fadeOut('fast', function() {
            $('.forgotBox').fadeOut('fast');
            $('.loginBox').fadeIn('fast');
            $('.button-facebook').fadeIn('fast');
            $('.division').fadeIn('fast');
            $('.register-footer').fadeOut('fast',function(){
                $('.login-footer').fadeIn('fast');
            });

            $('.modal-title').html('Welcome back!');
            $('.button-facebook').html('Login with Facebook');
            $('.tooltip-test').hide();
            $(".signupform").collapse('hide');
        });
         $('.error').removeClass('alert alert-danger').html('');
    }

    function showForgotForm(){
        $('.loginBox').fadeOut('fast',function(){
            $('.registerBox').fadeOut('fast');
            $('.button-facebook').fadeOut('fast');
            $('.division').fadeOut('fast');
            $('.forgotBox').fadeIn('fast');
            $('.register-footer').fadeIn('fast');
            $('.modal-title').html('Reset your password');
        });
    }

    function openLoginModal(){
        showLoginForm();
        setTimeout(function(){
            $('#loginModal').modal('show');
        }, 230);

    }
    function openRegisterModal(){
        showRegisterForm();
        setTimeout(function(){
            $('#loginModal').modal('show');
        }, 230);
    }

    function loginAjax(){
        /*   Remove this comments when moving to server
        $.post( "/login", function( data ) {
                if(data == 1){
                    window.location.replace("/home");
                } else {
                     shakeModal();
                }
            });
        */

    /*   Simulate error message from the server   */
         shakeModal();
    }

    function shakeModal(){
        $('#loginModal .modal-dialog').addClass('shake');
                 $('.error').addClass('alert alert-danger').html("Invalid email/password combination");
                 $('input[type="password"]').val('');
                 setTimeout( function(){
                    $('#loginModal .modal-dialog').removeClass('shake');
        }, 1000 );
    }