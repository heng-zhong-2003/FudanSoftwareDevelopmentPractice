const MyComponent = {
    template: `<div> Hello from MyComponent! </div>`
};

const app1= {
  template:`
  <a class="navbar-brand" v-bind:href="index"> $[ message ]</a>
  `,
  data(){
    return{
      message:"Home",
      index:'http://127.0.0.1:5000/pj',
    };
  },
  delimiters: ['$[', ']']
};

const app2= {
  template:`
  <li class="nav-item active">
    <a class="nav-link" v-bind:href="about">About
      <span class="sr-only">(current)</span>
    </a>
  </li>
  `,
  data(){
    return{
      about:'http://127.0.0.1:5000/pj/about',
    };
  },
};


const Header_1 = {
    template: `
<nav class="navbar navbar-expand-lg navbar-light bg-primary">
  <div id=app1>
    <app1></app1>
  </div>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
<div class="collapse navbar-collapse" id="navbarNavDropdown">
  <ul class="navbar-nav">
    <li class="nav-item">
      <div id=app2>
        <app2></app2>
      </div>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="#">选项1</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="#">选项2</a>
    </li>
    <li class="nav-item dropdown">
      <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        Dropdown link
      </a>
      <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
        <a class="dropdown-item" href="#">Action</a>
        <a class="dropdown-item" href="#">Another action</a>
        <a class="dropdown-item" href="#">Something else here</a>
      </div>
    </li>
  </ul>
</div>
</nav>
  `,
  components:{
    app1,app2
  }
};

