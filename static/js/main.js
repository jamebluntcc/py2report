<script>
        $(document).ready(function(){
            $('.table').DataTable();
        });
</script>
<script>
        // for each single plot
        $(".fancybox-effects-d").fancybox({
            padding: 0,
            openEffect : 'elastic',
            openSpeed  : 150,
            closeEffect : 'elastic',
            closeSpeed  : 150,
            closeClick : true,
            helpers : {
                overlay : null
            }
        });
        $(document).ready(function() {
            /*
             *   Examples - images
             */
            $("a.example2").fancybox({
                'overlayShow'	: true,
                'transitionIn'	: 'elastic',
                'transitionOut'	: 'elastic'
            });

            $("a[rel=example_group]").fancybox({
                'transitionIn'		: 'none',
                'transitionOut'		: 'none',
                'titlePosition' 	: 'over',
                'titleFormat'		: function(title, currentArray, currentIndex, currentOpts) {
                    return '<span id="fancybox-title-over">Image ' + (currentIndex + 1) + ' / ' + currentArray.length + (title.length ? ' &nbsp; ' + title : '') + '</span>';
                }
            });
        });
    </script>
    <script type="text/javascript">
        $(function(){
            //纵向，默认，移动间隔2
            $('div.albumSlider').albumSlider();
            //横向设置
            // $('div.albumSlider-h').albumSlider({direction:'h',step:3});
        });
    </script>