<script lang="ts">
    import { Input } from "$lib/components/ui/input";
    import { Button } from "$lib/components/ui/button/index.js";
    import MapContainer from "$lib/components/map/MapContainer.svelte";
    import Disneydashboard from '../routes/Disneydashboard.svelte';

     let popup = false;
     let email = "Email@mail.com";
     let name = "Name"
     let inputemail="";
     let inputname="";
     let isLogin=false;
 
     const login=()=>{
         if (isLogin){
             logout();
         }else{
             popup=true;
         }
     }
     const closePopup = () => {
         popup = false; 
     };
     const confirmed=()=>{
         if(inputname.trim()&&inputemail.trim()){
             name  = inputname;
             email = inputemail;
             popup =false;
             isLogin=true;
         }else{
             alert("Please enter valid name and email!");
         }
     }
     const logout=()=>{
         name = "Name"; 
         email = "Email@mail.com";
         inputname = "";
         inputemail = "";
         isLogin = false; 
     }
 
 </script>
 
 <main class="main">
     <div class="header">
         <div class="side-nav">
             <div class="icon">
                 <img src="/src/image/apple-touch-icon.png" alt="系统标志" class="wicon">
                 <h1>智能交通管理系统</h1>
             </div>
             <div class="user">
                 <img src="/src/image/user.png" alt="userphoto" class="user-image">
                 <div>
                     <h2 class="user_name"> {name}</h2>
                     <p class="user_email">{email}</p>
                 </div>
             </div>
             <ul>
                 <li ><img src="/src/image/dashboard.png" alt="dashboard"><p>Dashboard</p></li>
                 <li><img src="/src/image/reports.png" alt="reports"><p>Reports</p></li>
                 <li><img src="/src/image/messages.png" alt="message"><p>Message</p></li>
                 <li><img src="/src/image/projects.png" alt="project"><p>Our Projects</p></li>
                 <li><img src="/src/image/setting.png" alt="setting"><p>Settings</p></li>
             </ul>
 
             <ul>
                 <li><img src="/src/image/logout.png" alt="log" >
                     <button class="login-button" on:click={login}>
                         {isLogin ? "Logout" : "Login"}
                     </button>
                 </li>
             </ul>  
         </div>
         {#if popup}
             <div id="popup-modal" class="modal">
                 <div class=modal-content>
                     <button class="close-button" on:click={closePopup}>✖</button>
                     <h1> Welcome {inputname}</h1>
                     <Input type="name" placeholder="name" class="max-w-xs" bind:value={inputname}/>
                     <Input type="email" placeholder="email" class="max-w-xs mt-2 mb-3" bind:value={inputemail}/>
                     <Button variant="outline" on:click={confirmed}>Confirm</Button>
                 </div>             
             </div>
         {/if}
         <div class="map-container">
            <div style="border: 1px solid #ddd; padding: 10px;">
              <MapContainer />
            </div>
         </div>  
         <div class = "hot-disney">

         <div style="border: 1px solid #ddd; padding: 10px;">
              <Disneydashboard/>
         </div>
     </div>    
 
     
 </main>
 
 <style>
 :global(body) {
     padding: 0;
     box-sizing: border-box;
     font-family: 'Poppins', sans-serif;
     margin: 0;
    }

 .main {
    display: flex;
    flex-direction: row;   /* 子元素垂直排列 */
    height: 100vh;          /* 占满视口高度 */
    }
 
 .header {
    width:100%;
    height:100vh;
    background: url(/src/image/webpage.png);
    background-position: center;
    background-size: cover;
    }
 
 .side-nav{
    width: 250px;  
    height: 100%;
    position: fixed;
    top: 0;
    left: 0;
    padding: 30px 15px;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(5px);
    display: flex;
    justify-content: space-between;
    flex-direction: column;
    transition: none;
    }
 
 .icon{
     display:flex;
     align-items: center;
     justify-content: space-between;
     font-size: 12px;
     padding: 10px;
     margin-left: auto;
     margin-right: auto;
     overflow: hidden;
     width: 90%;
     margin: 0;
    }
 
 .icon h1{
     white-space: nowrap;
     display: block;
     font-size: 19px;
     font-weight: bold;
    }
 
 .wicon{
     width: 30px;
     height: 30px;
     margin:auto;
     display:block;
    }
 
 .user{
     display:flex;
     align-items: center;
     justify-content: space-between;
     font-size: 12px;
     padding: 10px;
     border-radius: 8px;
     overflow: hidden;
     width: 90%;
     margin: 0;
     background: rgb(255,255,255,0.2);
     backdrop-filter: blur(5px);
    }
 
 .user h2{
     font-size: 15px;
     font-weight: 600;
     white-space: nowrap;
    }
 
 .user-image{
     width:40px;
     border-radius: 50%;
     margin: auto;
    }
 
 .user div{
     display: block;
    }
 
 ul li {
    margin: 30px 0;
    display: flex;
    align-items: center;
    justify-content: flex-start;  
    cursor: pointer;
    }

 ul li p {
    white-space: nowrap;
    display: block; 
    }

 ul li img {
    width: 30px;
    margin-right: 10px; 
    }

 .login-button {
     background: none; 
     border: none; 
     color: inherit; 
     cursor: pointer; 
     padding: 0; 
     text-align: left; 
     font-size: inherit; 
    }
 
 .modal {
     position: fixed;
     top: 50%;
     left: 50%;
     transform: translate(-50%, -50%);
     background: rgb(255,255,255,0.2);
     backdrop-filter: blur(5px);
     padding: 10px;
     border-radius: 8px;
     box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
     z-index: 1000; 
     align-items: center;   
     width:300px;
    }
 
 .modal-content{
     padding:10px;
     display: flex;
     flex-direction: column;
     align-items: center;
    }
 
 .close-button {
     position: absolute;
     top: 10px;
     right: 10px;
     background: none;
     border: none;
     font-size: 20px;
     cursor: pointer;
     color: #000000;
    }
 
 .modal-content h1{
     font-size: 20px;
     font-weight: bold;
     margin-bottom: 10px;
    }

 .map-container {
     flex:1;
     margin-left: 250px;  
     padding: 2px;
    }
 </style>
 