var vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        host,
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        tab_content: {
            detail: true,
            pack: false,
            comment: false,
            service: false
        },
        sku_id: '',
        sku_count: 1,
        sku_price: price,
        cart_total_count: 0, // 购物车总数量
        cart: [], // 购物车数据
        hots: [], // 热销商品
        cat: cat, // 商品类别
        comments: [], // 评论信息
        score_classes: {
            1: 'stars_one',
            2: 'stars_two',
            3: 'stars_three',
            4: 'stars_four',
            5: 'stars_five',
        }
    },

    computed: {
        sku_amount: function () {
            return (this.sku_price * this.sku_count).toFixed(2);
        }
    },

    mounted: function () {
        this.get_sku_id();

        // 添加用户浏览历史记录
        if (this.user_id) {
            axios.post(this.host+'/browse_histories/', {
                sku_id: this.sku_id
            }, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                }
            })
        }else {
            alert('没有登陆')
        }

        this.get_cart();
        this.get_comments();
    },

    methods: {
        // 退出
        logout: function () {
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },

        // 控制页面标签页展示
        on_tab_content: function (name) {
            this.tab_content = {
                detail: false,
                pack: false,
                comment: false,
                service: false
            };
            this.tab_content[name] = true;
        },
        // http://www.meiduo.site:8080/goods/10.html
        // 从路径中提取sku_id
        get_sku_id: function () {
            var re = /^\/goods\/(\d+).html$/;  // /goods/10.html
            this.sku_id = document.location.pathname.match(re)[1];//[1] 把数字10提取出来
        },

        // 减小数值
        on_minus: function () {
            if (this.sku_count > 1) {
                this.sku_count--;
            }
        },

        // 添加购物车
         add_cart: function() {
            let data = {
                sku_id: parseInt(this.sku_id),
                count: this.sku_count
            };
            let config = {
                headers: { // 通过请求头往服务器传递登录状态
                    'Authorization': 'JWT ' + this.token
                },
                withCredentials: true   // 注意： 跨域请求传递cookie给服务器
            };
            axios.post(this.host+'/cart/', data, config)
                .then(response => {
                    alert('添加购物车成功');
                    this.cart_total_count += response.data.count;
                })
                .catch(error => {
                    alert('添加购物车失败');
                    console.log(error.response.data);
                })
        },

        // 获取购物车数据
        get_cart: function () {

        },

        // 获取商品评价信息
        get_comments: function () {

        }
    }
});