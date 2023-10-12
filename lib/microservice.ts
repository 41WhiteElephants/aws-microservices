import { ITable } from "aws-cdk-lib/aws-dynamodb";
import { Runtime } from "aws-cdk-lib/aws-lambda";
import { NodejsFunction, NodejsFunctionProps } from "aws-cdk-lib/aws-lambda-nodejs";
import { PythonFunction, PythonFunctionProps} from "@aws-cdk/aws-lambda-python-alpha";
import { Construct } from "constructs";
import { join } from "path";

interface SwnMicroservicesProps {
    productTable: ITable;
    basketTable: ITable;
    orderTable: ITable;
}

export class SwnMicroservices extends Construct {

  public readonly productMicroservice: NodejsFunction;
  public readonly basketMicroservice: NodejsFunction;
  public readonly orderingMicroservice: NodejsFunction;

  constructor(scope: Construct, id: string, props: SwnMicroservicesProps) {
    super(scope, id);

    // product microservices
    this.productMicroservice = this.createProductFunction(props.productTable);
    // basket microservices
    this.basketMicroservice = this.createBasketFunction(props.basketTable);
    // ordering Microservice
    this.orderingMicroservice = this.createOrderingFunction(props.orderTable);
  }


    private createProductFunction(productTable: ITable) : PythonFunction {
      const productFunctionProps: PythonFunctionProps = {
        environment: {
          PRIMARY_KEY: 'id',
          DYNAMODB_TABLE_NAME: productTable.tableName
        },
        runtime: Runtime.PYTHON_3_9,
        entry: join(__dirname, '/../src/product'),
        handler: "lambda_handler",
        index: 'product.py'
      }

      const productFunction = new PythonFunction(this, 'productLambdaFunction', {
        ...productFunctionProps
      });

      productTable.grantReadWriteData(productFunction);

      return productFunction;
    }

  private createBasketFunction(basketTable: ITable) : PythonFunction {
    const basketFunctionProps: PythonFunctionProps = {
      environment: {
          PRIMARY_KEY: 'userName',
          DYNAMODB_TABLE_NAME: basketTable.tableName,
          EVENT_SOURCE: "com.swn.basket.checkoutbasket",
          EVENT_DETAIL_TYPE: "CheckoutBasket",
          EVENT_BUS_NAME: "SwnEventBus"
      },
      runtime: Runtime.PYTHON_3_9,
      entry: join(__dirname, '/../src/basket'),
      handler: "lambda_handler",
      index: 'basket.py'
    }

    const basketFunction = new PythonFunction(this, 'basketLambdaFunction', {
      ...basketFunctionProps
    });

    basketTable.grantReadWriteData(basketFunction);
    return basketFunction;
  }

  private createOrderingFunction(orderTable: ITable) : PythonFunction {
    const orderingFunctionProps: PythonFunctionProps = {
        environment: {
            PRIMARY_KEY: 'userName',
            SORT_KEY: 'orderDate',
            DYNAMODB_TABLE_NAME: orderTable.tableName,
        },
      runtime: Runtime.PYTHON_3_9,
      entry: join(__dirname, '/../src/ordering'),
      handler: "lambda_handler",
      index: 'ordering.py'
    }

    const orderFunction = new PythonFunction(this, 'orderingLambdaFunction', {
      ...orderingFunctionProps
    });

    orderTable.grantReadWriteData(orderFunction);
    return orderFunction;
  }

}
