
// 当页面渲染完毕后马上调用下面的函数，这个函数是在当前页面 - 设置 - 生命周期 - 页面加载完成时中被关联的。

export function didMount() {
  console.log(`「页面 JS」：当前页面地址 ${location.href}`);
  //console.log(`「页面 JS」：当前页面 id 参数为 ${this.state.urlParams.id}`);
  // 更多 this 相关 API 请参考：https://www.yuque.com/yida/support/ocmxyv#OCEXd
  // document.title = window.loginUser.userName + ' | 宜搭';

  let x_hash = location.hash
  //console.log(x_hash.length)

  if (x_hash.length != 0) {
    this.$('textField_lywahqdo').setValue(location.hash.substr(5))
  }  
    
}

var getJSON = async (url) => {
  let response = await fetch(url);
  //console.log(response)
  let JSON = await response.json();
  //console.log(JSON)
  return JSON
}

export function onchangeNo() {
  // 獲取輸入框的值
  if (this.$('textField_lu6unmsk').getValue().length > 0) {
    let sn = this.$('textField_lu6unmsk').getValue();
    let enly_api = "https://api.syf.com.tw/api/get_enly_Ship_forApi.php?no=";
    let totalRealCost = 0;

    // 發送GET請求並處理返回的Promise
    getJSON(enly_api + sn).then(result => {
      if (result != null) {
        // 計算totalRealCost
        totalRealCost = result.reduce((sum, item) => sum + parseInt(item.realcost), 0);
        // 設置輸出框的值為計算結果
        this.$('textField_m04w5r59').setValue(totalRealCost + " 元");
      } else {
        // 如果result為null，設置輸出框的值為 "--"
        this.$('textField_m04w5r59').setValue("--");
      }
    });
  }
}

export function onchangeCat(){
  let $cat = this.$('selectField_m0p0qtjp').getValue()
  let $tableField_m0p0qtju = this.$('tableField_m0p0qtju')
  //API 取值定義變數-參閱宜搭文件https://docs.aliwork.com/docs/yida_support/lbtl0t/rrwdug/agb8im#M07ak
  let params = {
    formUuid: "FORM-ZK866D91TK0BN686BVK7R8UOYJUU3IFPMO2ILH1",
    appType: "APP_X1B03GO5YIPWFBC76PQW",
    searchFieldJson: '{"textField_m060dv8x":"' + $cat+'"}',
    //createFrom:"2017-01-01",
    //createTo: "2024-09-01",
    currentPage: 1,
    pageSize:100,
    //dynamicOrder: {"dateField_li2iiqgz":"-"}
  }
  
  // 調用數據源的load方法，傳入參數params，並處理返回的Promise
  this.dataSourceMap.myDatasource.load(params).then((response) => {
    //console.log(response) // 調試用，輸出response

    let $totalCount = response.totalCount; // 獲取總數量
    let $Data = []; // 初始化數據數組
    let order_sn; // 初始化order_sn變量

    //console.log(response) // 調試用，輸出response

    // 遍歷response.data，將每個item的formData屬性值添加到$Data數組中
    response.data.forEach(item => {
      $Data.push(item.formData);
    });

    // 如果總數量小於等於100，輸出$Data數組
    if ($totalCount <= 100) {
      console.log($Data);
    } else {
      // 計算總頁數，向上取整
      let totalPage = Math.ceil($totalCount / 100);
      console.log($totalCount); // 輸出總數量

      // 從第2頁開始遍歷到總頁數
      for (var i = 2; i <= totalPage; i++) {
        params.currentPage = i; // 設置當前頁數
        // 調用數據源的load方法，傳入更新後的參數params，並處理返回的Promise
        this.dataSourceMap.myDatasource.load(params).then((response) => {
          // 遍歷response.data，將每個item的formData屬性值添加到$Data數組中
          response.data.forEach(item => {
            $Data.push(item.formData);
          });
          //console.log(response) // 調試用，輸出response
          //console.log($Data) // 調試用，輸出$Data數組   
        });
      }
    }
    // 設置一個定時器，每隔500毫秒執行一次order_sn_f函數 (配合API進行非同步執行)
    var run_order_sn = setInterval(order_sn_f, 500);

    let order_l = 0; // 初始化計數器

    // 定義order_sn_f函數
    function order_sn_f() {
      // 如果計數器ti大於等於$Data數組的長度
      if (order_l >= $Data.length) {        
        clearInterval(run_order_sn); // 清除定時器        

        ///透過工單號取運費加總
        //*** 取工單號填入子表單****/
        order_sn.sort((a, b) => b.textField_li2hrlly - a.textField_li2hrlly)

        // 如果陣列長度大於50，取前50筆
        if (order_sn.length > 50) {
          order_sn = order_sn.slice(0, 50);
        }
        console.log(order_sn); // 輸出order_sn數組

        let tableV = []; // 初始化tableV數組

        // 遍歷order_sn數組
        order_sn.forEach(item => {
          let tableD = {}; // 初始化tableD物件
          tableD.textField_m0p0qtjv = item.textField_li2hrlly; // 設置tableD的textField_m0p0qtjv屬性
          tableD.textField_m0ypx4wr = item.textField_li2hrlm8; // 設置tableD的textField_m0ypx4wr屬性
          tableD.textField_m0ypx4ws = item.textField_li2hrlmc; // 設置tableD的textField_m0ypx4ws屬性

          let sn = item.textField_li2hrlly; // 獲取sn值
          let enly_api = "https://api.syf.com.tw/api/get_enly_Ship_forApi.php?no="; // API URL
          let totalRealCost = 0; // 初始化totalRealCost

          // 發送GET請求並處理返回的Promise
          getJSON(enly_api + sn).then(result => {
            if (result != null) {
              // 計算totalRealCost
              totalRealCost = result.reduce((sum, item) => sum + parseInt(item.realcost), 0);
              // 設置tableD的numberField_m0p0qtjx屬性為計算結果
              tableD.numberField_m0p0qtjx = totalRealCost;
            } else {
              // 如果result為null，設置tableD的numberField_m0p0qtjx屬性為0
              tableD.numberField_m0p0qtjx = totalRealCost;
            }
            tableV.push(tableD); // 將tableD添加到tableV數組中
          });
        });

        console.log(tableV.length); // 輸出tableV數組的長度

        var run_set_table = setInterval(set_table, 500); // 設置定時器，每隔500毫秒執行一次set_table函數

        let table_l = 0; // 初始化table_l

        // 定義set_table函數
        function set_table() {
          if (table_l >= order_sn.length) {
            clearInterval(run_set_table); // 清除定時器
            $tableField_m0p0qtju.setValue(tableV); // 設置$tableField_m0p0qtju的值為tableV
          } else {
            table_l = tableV.length; // 更新table_l為tableV的長度
          }
        }

      } else {
        order_sn = []; // 初始化order_sn數組
        // 遍歷$Data數組，將每個元素的textField_li2hrlly屬性值添加到order_sn數組中
        $Data.forEach(item => {
          let push_item={}
          push_item.textField_li2hrlly = item.textField_li2hrlly //工單號
          push_item.textField_li2hrlmc = item.textField_li2hrlmc //工單號
          push_item.textField_li2hrlm8 = item.textField_li2hrlm8 //訂單數量
          
          order_sn.push(push_item);
        });
        order_l = order_sn.length; // 更新計數器為order_sn數組的長度
      }
    }    
  })
  //console.log('onClick');
}
