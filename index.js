var pyshell =  require('python-shell')

function execute() {
  pyshell.run('hello.py',  function  (err, results)  {
   if  (err)  throw err;
   console.log('hello.py finished.');
   $('#tag').html(results);
   console.log('results', results);
  });
}

  execute();
