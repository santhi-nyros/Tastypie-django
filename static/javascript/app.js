"use strict";

var app = angular.module("myApp", ['ngAnimate', 'ngTouch','ngRoute'], function ($interpolateProvider) {
        $interpolateProvider.startSymbol("{[{");
        $interpolateProvider.endSymbol("}]}");
    }
);



app.config(function ($routeProvider) {
    $routeProvider
        .when("/", {
            templateUrl: "templates/index.html",

        })
        // .when("/search",{
        //   templateUrl: "static/js/app/views/car_index.html",
        //   controller: "searchController",


        // })
        // .when("/seemore",{
        //   templateUrl: "static/js/app/views/car_index1.html",
        //   // controller: "CityController",

        // })
        .otherwise({
            redirectTo: '/'
        })
})




app.directive('whenscrollends', function() {
    return {
        restrict: "A",
        link: function(scope, element, attrs) {
            var visibleHeight = element.height();
            var threshold = 100;

            element.scroll(function() {
                var scrollableHeight = element.prop('scrollHeight');
                var hiddenContentHeight = scrollableHeight - visibleHeight;

                if (hiddenContentHeight - element.scrollTop() <= threshold) {
                    // Scroll is almost at the bottom. Loading more rows
                    scope.$apply(attrs.whenscrollends);
                }
            });
        }
    };
});


app.controller('AppController', ['$http','$scope','$window', function($http, $scope){
  var data = [];
  $scope.flags = {};
  $scope.comments = '';
  // $scope.comment_txt = '';
  // $scope.showDetails/ = true;


//converting to datetime into time
  $scope.getHours = function(actionDate)
  {

      var now = new Date();
      var days = parseInt(Math.abs(now - new Date(actionDate+'Z')) / (1000 * 60 * 60 * 24));
      if(days == 0)
      {
        var hours = parseInt(Math.abs(now - new Date(actionDate+'Z')) / (1000 * 60 * 60));

        if(hours == 0)
        {
          var minutes = (now - new Date(actionDate+'Z')) / (1000 * 60);
          minutes = Math.floor(minutes)
          if(minutes <= 0){
            return "now"
          }
          else{
            return Math.floor(minutes) +" mins";
          }
        }
        else
        {
          return hours + " hrs ago";
        }
      }
      else
        return days + " day(s) ago";
  };



// get method for posts data
    $scope.totalDisplayed = 0
    $scope.get_post = function() {
       $http.get('/api/v1/posts/').then(function(response) {
            $scope.posts = response.data.objects
            var count = $scope.posts.length;

            while(count) {
              data[count] = count--;
            }
            $scope.totalDisplayed += 4;

            for(var i=0;i<$scope.posts.length;i++){
              // get time
              var time = $scope.getHours($scope.posts[i]['created'])
              $scope.posts[i]['time'] = time;
              //end


            }
            $scope.data = $scope.posts;
        });
    };

    $scope.get_post();


// data loading on scorlling
    function loadmore() {
      var windowHeight = "innerHeight" in window ? window.innerHeight
              : document.documentElement.offsetHeight;
          var body = document.body, html = document.documentElement;
          var docHeight = Math.max(body.scrollHeight,
              body.offsetHeight, html.clientHeight,
              html.scrollHeight, html.offsetHeight);
          var windowBottom = windowHeight + window.pageYOffset;
          if (windowBottom >= docHeight) {
            // alert('bottom reached');
              $scope.get_post();
          }
    }
    $(function () {
        $(window).scroll(loadmore);
      loadmore();
    });


//tabs
      $scope.tabs = [{
           title: "static/images/stats.png",
            url: 'one.tpl.html'
        },
        {
            title: "static/images/temple.png",
            url: 'two.tpl.html'
        }, {
            title: "static/images/flask.png",
            url: 'three.tpl.html'
        }, {
            title: "static/images/ball.png",
            url: 'four.tpl.html'
        },{
           title: "static/images/clapper.png",
            url: 'five.tpl.html'
        }
    ];

    $scope.currentTab = 'one.tpl.html';

    $scope.onClickTab = function (tab) {
        $scope.currentTab = tab.url;
    }

    $scope.isActiveTab = function(tabUrl) {
        return tabUrl == $scope.currentTab;
    }

    // $scope.get_comments = function(post){
    //   $scope.flags[post.id] = !$scope.flags[post.id];
    //   if ($scope.flags[post.id] == true){
    //     $scope.getComments(post);
    //   }

    // }

// saving posts
    $scope.postSumbit = function(){
       $scope.image = $("#image").prop("files")[0]
       $scope.video = $("#video").prop("files")[0]
        if ($scope.text != undefined && $scope.text != '' || $scope.image != undefined || $scope.video != undefined){
          var fd = new FormData();
          fd.append('text', $scope.text);
          fd.append('image', $("#image").prop("files")[0]);
          fd.append('video', $("#video").prop("files")[0]);

          $.ajax({
            url: '/api/v1/posts/',
            contentType: false,
            processData: false,
            headers: {
              'X-HTTP-Method-Override': 'POST',
            },
            method: 'POST',
            data: fd,
            beforeSend: function(jqXHR, settings) {
              jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            },
            success: function(data, textStatus, jqXHR) {
              $('#myModal').find('input[type="file"]').val('');
              $('#myModal').find('textarea').val('');
              $scope.text =''

              $('#myModal').modal('hide');
              $scope.get_post();
            }
          });
          }else{
            alert("This post appears to be blank. Please write something or attach a link or photo to post.")
          };
      };


      //slider images
       $scope.slides = [
            {image: '/static/images/slide1.jpg', description: 'Love and relationship quotes',text:'Community · 1,306,171 likes'},
            //{image: '/static/images/slide2.jpg', description: "Your loss, I'm awesome",text:"Community · 665,754 likes"},
            {image: '/static/images/slide3.jpg', description: 'Cute Relationships',text:'Community · 358,062 likes'},
            {image: '/static/images/slide4.png', description: 'Photography From Around The World',text:'Website · 637,251 likes'},
            {image: '/static/images/slide5.jpg', description: 'Wonderful Quotes',text:'Media/news company · 1,255,878 likes'}
        ];

        $scope.direction = 'left';
        $scope.currentIndex = 0;

        $scope.setCurrentSlideIndex = function (index) {
            $scope.direction = (index > $scope.currentIndex) ? 'left' : 'right';
            $scope.currentIndex = index;
        };

        $scope.isCurrentSlideIndex = function (index) {
            return $scope.currentIndex === index;
        };

        $scope.prevSlide = function () {
            $scope.direction = 'left';
            $scope.currentIndex = ($scope.currentIndex < $scope.slides.length - 1) ? ++$scope.currentIndex : 0;
        };

        $scope.nextSlide = function () {
            $scope.direction = 'right';
            $scope.currentIndex = ($scope.currentIndex > 0) ? --$scope.currentIndex : $scope.slides.length - 1;
        };

// get and post method of comments
      $scope.getComments = function(post){
        var url = '/api/v1/posts/'+post.id+'/get_comments/'
         $http.get(url).then(function(response) {

            $scope.comments = response.data.objects;

            $('#comment_'+post.id).empty();

            for(var i=0;i<$scope.comments.length;i++){

              $scope.post_id = $scope.comments[i].post_id;
              var time = $scope.getHours($scope.comments[i].created)
              $scope.comments[i]['time'] = time;
              if (post.image == 'undefined'){
                $scope.comments[i]['img'] = 'static/images/default.jpg';
              }else{
                $scope.comments[i]['img'] = post.image;
              }
            };
        });
      }

      $scope.postComment = function(post,comment){
        if(comment != undefined && comment != ''){
          var postData = {'post_id':post,'comment':comment}
          $.ajax({
            url: '/api/v1/comments/',
            type: "POST",
            data : JSON.stringify(postData),
            processData: false,
            contentType: 'application/json',
            beforeSend: function(jqXHR, settings) {
              jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            },
            success: function(data, textStatus, jqXHR) {
              $('.myComment').find('input[type="text"]').val('');
              $scope.getComments(post);
            }
          });
        }else{
          alert("Please text your comment here")
        }
      }
}]);


app.animation('.slide-animation', function () {
        return {
            beforeAddClass: function (element, className, done) {
                var scope = element.scope();

                if (className == 'ng-hide') {
                    var finishPoint = element.parent().width();
                    if(scope.direction !== 'right') {
                        finishPoint = -finishPoint;
                    }
                    TweenMax.to(element, 0.5, {left: finishPoint, onComplete: done });
                }
                else {
                    done();
                }
            },
            removeClass: function (element, className, done) {
                var scope = element.scope();

                if (className == 'ng-hide') {
                    element.removeClass('ng-hide');

                    var startPoint = element.parent().width();
                    if(scope.direction === 'right') {
                        startPoint = -startPoint;
                    }

                    TweenMax.fromTo(element, 0.5, { left: startPoint }, {left: 0, onComplete: done });
                }
                else {
                    done();
                }
            }
        };
    });
