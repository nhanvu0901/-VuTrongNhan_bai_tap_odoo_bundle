odoo.define('website.cart_frontend', function (require) {
    if(window.location.href.includes("/shop/cart")){
        console.log("Hello")
        function insertAfter(newNode, existingNode) {
            existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
        }


        let rows = document.getElementById("cart_products")
        let data = rows.getElementsByTagName("tr")
        let list_product = [];
        for (let i = 1; i < data.length; i++) {
            if(data[i].innerHTML.includes('<a href=')){
                var doc =new DOMParser().parseFromString(data[i].cells[1].outerHTML,"text/xml")

                var url = new DOMParser().parseFromString(doc.firstElementChild.firstElementChild.innerHTML,"text/xml").firstChild.attributes.href.nodeValue
                let info_string= url.split('/')[2]

                let name_array = info_string.split('-')

                if(info_string.includes("#")){
                   list_product.push({
                       product_id:name_array[name_array.length-1].substring(0,name_array[name_array.length-1].indexOf('#')),
                       product_quantity : data[i].cells[2].firstElementChild.childNodes[3].value
                   })
                }
                else{
                   list_product.push(
                       {
                       product_id:name_array[name_array.length-1],
                        product_quantity : data[i].cells[2].firstElementChild.childNodes[3].value
                       }
                   )
                }
                    }
                }
        console.log(list_product)

        param={
            data:JSON.stringify(list_product),

        }
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.open("POST", "https://odoo.website/cart");
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.onreadystatechange = function () {
                if (xmlhttp.readyState === 4) {
                    if (xmlhttp.status === 200) {
                       // let response =JSON.parse(JSON.parse(xmlhttp.responseText).result)
                        console.log(xmlhttp.responseText)
                        if(xmlhttp.responseText){
                            let money = JSON.parse(JSON.parse(xmlhttp.responseText).result)
                            let total_node = document.getElementById("order_total")
                            let money_span = document.createElement("TR")
                            money_span.style.color='red'

                            if(typeof(money) === "number"){
                                let text = document.createElement("TD")
                                text.textContent ="Final price after sale:"
                                text.classList.add("text-right")
                                money_span.appendChild(text)
                                let money_node = document.createElement("TD")
                                money_node.textContent = money +"$"
                                money_node.classList.add("text-xl-right")
                                money_span.appendChild(money_node)
                            }
                            else{
                                money.forEach(item=>{
                                    let para = document.createElement("P")
                                    para.innerHTML = item
                                    money_span.appendChild(para)
                                })
                            }




                            insertAfter(money_span,total_node)
                        }


                    }
                }
            };
        xmlhttp.send(JSON.stringify(param))



    }


});

