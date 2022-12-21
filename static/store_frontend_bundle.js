odoo.define('website.store_frontend', function (require) {
    if(window.location.href.includes("/shop/") && !window.location.href.includes("/shop/cart")){

        let url = window.location.href
        let info_string= url.split('/')[4]
        let name_array = info_string.split('-')
         let product_id_string =''
        if(name_array[name_array.length-1].includes("#")){
           product_id_string=  name_array[name_array.length-1].substring(0,name_array[name_array.length-1].length-6)
        }
        else{
             product_id_string=  name_array[name_array.length-1]
        }

        param={
            data:product_id_string,

        }
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.open("POST", "https://odoo.website/bundle");
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.onreadystatechange = function () {
                if (xmlhttp.readyState === 4) {
                    if (xmlhttp.status === 200) {
                       let response =JSON.parse(JSON.parse(xmlhttp.responseText).result)
                        console.log(response)
                        let box = document.getElementsByClassName("product_price")
                       for (var i = 0; i < response.length; i++){

                           if(response[i].bundle_type === 'total'){
                               let start_date = null
                               let end_date = null
                               if(response[i].start_time !== '' || response[i].end_time !== ''){
                                   start_date = new Date(response[i].start_time)
                                   end_date =  new Date(response[i].end_time)
                                   var today = new Date()
                                   if(today <= start_date || today >= end_date){
                                       continue
                                   }
                               }
                               let bundle_total = document.createElement("DIV")
                               bundle_total.classList.add("Total")

                               bundle_total.style.width="40vw"
                               let data = ''
                               let sum=0
                               let discount = response[i].discount_amount
                               let discount_container = document.createElement("DIV")
                               discount_container.classList.add('discount-container')
                               let disccount_span = document.createElement("DIV")
                                disccount_span.classList.add('discount-percent')
                               disccount_span.innerHTML ="Sale: " +response[i].discount_amount

                               bundle_total.appendChild(disccount_span)


                              const price_list =[]
                                response[i].products.forEach((product, index, arr)=>{
                                let image_frame = document.createElement("IMG")
                               image_frame.src = product.image_url
                                discount_container.appendChild(image_frame)
                                let span = document.createElement("SPAN")
                              span.classList.add('name-item')
                               if(index !== arr.length - 1){
                                data = product.product_name+" x"+product.quantity
                                span.innerHTML = data
                                discount_container.appendChild(span)
                                let plus = document.createElement("SPAN")
                                plus.innerHTML=" + "
                                plus.style.fontSize='2rem'
                                 discount_container.appendChild(plus)
                              }
                              else{
                                data = product.product_name+" x"+product.quantity
                               span.innerHTML = data
                                discount_container.appendChild(span)
                              }



                              price_list.push(
                                  {
                                      price:product.product_price,
                                      quantity:product.quantity
                                  }
                              )

                                });
                               let equal = document.createElement("SPAN")
                               equal.innerHTML = "="
                            discount_container.appendChild(equal)

                             price_list.forEach(item=>{
                               sum += parseInt(item.price)* parseInt(item.quantity)
                             })


                          if(discount.charAt(discount.length-1)==='%'){
                              let percent =parseInt(response[i].discount_amount.substring(0,response[i].discount_amount.length))
                             let math = sum - sum * (percent /100)

                             // data += "=" +math.toString()
                             let span = document.createElement("SPAN")
                              span.classList.add('price')
                             span.innerHTML =  math.toString()
                              discount_container.appendChild(span)


                           bundle_total.appendChild(discount_container)
                           }
                          else{
                              let amount =parseInt(response[i].discount_amount)
                             let math = sum - amount

                             // data += "=" +math.toString()
                             let span = document.createElement("SPAN")

                              span.innerHTML =  math.toString()
                              span.classList.add('price')
                              discount_container.appendChild(span)

                              bundle_total.appendChild(discount_container)



                          }
                           box[0].appendChild(bundle_total)
                           }
                            if(response[i].bundle_type === 'each'){
                                let start_date = null
                               let end_date = null
                               if(response[i].start_time !== '' || response[i].end_time !== ''){
                                   start_date = new  Date(response[i].start_time)
                                   end_date = new  Date(response[i].end_time)
                                   var today = new Date()
                                   if(today <= start_date || today >= end_date){
                                       continue
                                   }
                               }
                                 let bundle_each = document.createElement("DIV")
                                bundle_each.classList.add("Each")
                                bundle_each.style.width="40vw"
                                let bundle_discount = response[i].discount_amount
                                let discount_container = document.createElement("DIV")
                               discount_container.classList.add('discount-each')
                               discount_container.style.display="flex"
                               discount_container.style.flexDirection="column"
                               discount_container.style.justifyContent="center"
                               discount_container.style.alignContent="center"
                               let disccount_span = document.createElement("DIV")
                                disccount_span.classList.add('discount-percent')
                               disccount_span.innerHTML ="Multiple product"
                                bundle_each.appendChild(disccount_span)


                                const price_list_each =[]
                                response[i].products.forEach((product, index, arr)=>{
                                let product_container_each = document.createElement("DIV")
                                product_container_each.classList.add("product-container-each")
                                product_container_each.style.display="grid"
                                product_container_each.style.gridTemplateColumns = "auto auto auto"
                                product_container_each.style.justifyContent="space-between"

                                let image_name_container = document.createElement("DIV")
                                image_name_container.style.display="flex"
                                image_name_container.style.flexDirection="column"
                                let image_frame = document.createElement("IMG")
                               image_frame.src = product.image_url
                                image_name_container.appendChild(image_frame)
                                let span_name = document.createElement("SPAN")
                                span_name.innerHTML =  product.product_name
                                image_name_container.appendChild(span_name)
                                product_container_each.appendChild(image_name_container)


                                let discount_amout_span = document.createElement("SPAN")
                                discount_amout_span.style.color ="green"
                                discount_amout_span.innerHTML="Sale: "+ product.discount_value + `${bundle_discount.charAt(bundle_discount.length-1)==='%' ? "%":""}`
                                product_container_each.appendChild(discount_amout_span)

                                let span_money = document.createElement("DIV")
                                span_money.style.whiteSpace = "pre-line"
                                // calculate the sale and final money
                                let money_sale = ""
                                let money_sale_span = document.createElement("P")
                                let money_origin_span = document.createElement("P")
                                money_origin_span.style.textDecoration ="line-through"
                                 money_origin_span.style.color = "red"
                                 money_sale_span.style.color = "green"
                                let money_origin =product.product_price
                                money_origin_span.innerHTML = money_origin
                                span_money.appendChild(money_origin_span)
                                if(bundle_discount.charAt(bundle_discount.length-1)==='%'){
                                   money_sale = money_origin - money_origin* (parseInt(product.discount_value)/100)
                                   money_sale_span.innerHTML = money_sale
                                   span_money.appendChild(money_sale_span)
                                }
                                else{
                                     money_sale = money_origin - parseInt(product.discount_value)
                                   money_sale_span.innerHTML = money_sale
                                   span_money.appendChild(money_sale_span)
                                }
                                product_container_each.appendChild(span_money)
                                discount_container.appendChild(product_container_each)
                                bundle_each.appendChild(discount_container)




                                 price_list_each.push(product.product_price)


                                });
                            box[0].appendChild(bundle_each)
                            }

                            if(response[i].bundle_type==="tier"){
                                let start_date = null
                               let end_date = null
                               if(response[i].start_time !== '' || response[i].end_time !== ''){
                                   start_date = new  Date(response[i].start_time)
                                   end_date = new  Date(response[i].end_time)
                                   var today = new Date()
                                   if(today <= start_date || today >= end_date){
                                       continue
                                   }
                               }
                                let bundle_tier = document.createElement("DIV")
                                bundle_tier.classList.add("Tier")
                               bundle_tier.style.width="40vw"

                               let bundle_discount = response[i].discount_amount
                                 let disccount_span = document.createElement("DIV")
                                disccount_span.classList.add('discount-percent')
                               disccount_span.innerHTML ="BUY MORE GET MORE"
                                bundle_tier.appendChild(disccount_span)
                                let discount_container_tier = document.createElement("DIV")
                               discount_container_tier.classList.add('discount-each')
                               discount_container_tier.style.display="grid"
                               discount_container_tier.style.gridTemplateColumns="40% 60%"




                                let product_name = ''
                                response[i].products.forEach((product, index, arr)=> {

                                let image_frame = document.createElement("IMG")
                               image_frame.src = product.image_url
                               discount_container_tier.appendChild(image_frame)
                               product_name = product.product_name
                                })

                                let info_product_container = document.createElement("DIV")
                                info_product_container.style.display = "flex"
                                info_product_container.style.flexDirection = 'column'

                                let product_name_div = document.createElement("P")
                                product_name_div.innerHTML = product_name
                                info_product_container.appendChild(product_name_div)




                                let discount_info_container = document.createElement("DIV")
                                discount_info_container.style.display = "flex"
                                discount_info_container.style.flexDirection = "row"
                                discount_info_container.style.justifyContent = "center"
                                discount_info_container.style.alignSelf="baseline"
                                 discount_info_container.style.gap="5rem"
                                response[i].quantity.forEach((quantity, index, arr)=>{
                                    let quantity_info_container = document.createElement("DIV")
                                    quantity_info_container.style.border = "1px solid #444"
                                    quantity_info_container.style.borderRadius = '10px'
                                    quantity_info_container.style.width = '10rem'
                                     quantity_info_container.style.textAlign = 'center'

                                    let quanity_name = document.createElement("P")
                                    quanity_name.style.background ='rgba(115, 60, 8)'
                                    quanity_name.style.color = '#ffff'

                                    quanity_name.style.borderTopRightRadius='10px'
                                    quanity_name.style.borderTopLeftRadius='10px'

                                    if(quantity.Is_add_range === false){
                                        quanity_name.innerHTML ="Adds "+ quantity.Quantity +" items"
                                    }
                                    else{
                                        quanity_name.innerHTML ="Adds "+ quantity.Qty_start+"-"+quantity.Qty_end +" items"
                                    }
                                    quantity_info_container.appendChild(quanity_name)

                                     let quantity_discount = document.createElement("P")
                                      if(bundle_discount.charAt(bundle_discount.length-1)==='%'){
                                       quantity_discount.innerHTML = "Get " + quantity.Discount_value +"% OFF"
                                     }
                                     else{
                                         quantity_discount.innerHTML = "Get " + quantity.Discount_value +" OFF"
                                     }
                                     quantity_info_container.appendChild(quantity_discount)
                                    discount_info_container.appendChild(quantity_info_container)
                                    info_product_container.appendChild(discount_info_container)
                                });

                                discount_container_tier.appendChild(info_product_container)
                                bundle_tier.appendChild(discount_container_tier)



                            box[0].appendChild(bundle_tier)
                            }
                            document.head.innerHTML += `
                                          <style>
                                         @media screen and (min-width: 990px){
                                              .product__info-wrapper {
                                                padding: 0 0 0 0;
                                              }}
                                            .discount-container{
                                             display: flex;
                                             flex-direction: row;
                                             justify-content: flex-start;
                                             align-items: center;
                                            }
                                            .product_price img {
                                              height: 10vh;
                                            }
                                            .discount-percent{
                                                font-size: 2rem;
                                                color: red;
                                            }
                                            .discount-container .price{
                                                font-size: 2rem;
                                                color: red;
                                            }
                                           
                                          </style>`
                       }
                    }
                }
            };
        xmlhttp.send(JSON.stringify(param))


        // let price = document.getElementsByClassName("product_price")
        // let money_span = document.createElement("SPAN")
        // money_span.innerHTML ="Final price:"
        // price[0].appendChild(money_span)
    }


});

