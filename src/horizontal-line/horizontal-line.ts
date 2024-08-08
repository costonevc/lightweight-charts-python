import {
    DeepPartial,
    MouseEventParams
} from "lightweight-charts";
import { Point } from "../drawing/data-source";
import { Drawing, InteractionState } from "../drawing/drawing";
import { DrawingOptions } from "../drawing/options";
import { HorizontalLinePaneView } from "./pane-view";
import { GlobalParams } from "../general/global-params";
import { HorizontalLineAxisView } from "./axis-view";


declare const window: GlobalParams;

export class HorizontalLine extends Drawing {
    _type = 'HorizontalLine';
    _paneViews: HorizontalLinePaneView[];
    _point: Point;
    private _callbackName: string | null;
    _priceAxisViews: HorizontalLineAxisView[];

    protected _startDragPoint: Point | null = null;

    constructor(point: Point, options: DeepPartial<DrawingOptions>, protected saveDrawings: Function, callbackName=null) {
        super(options)
        this._point = point;
        this._point.time = null;    // time is null for horizontal lines
        this._paneViews = [new HorizontalLinePaneView(this)];
        this._priceAxisViews = [new HorizontalLineAxisView(this)];

        this._callbackName = callbackName;

        this._childHandleMouseUpInteraction = this._childHandleMouseUpInteraction.bind(this);
    }

    public get points() {
        return [this._point];
    }

    public updatePoints(...points: (Point | null)[]) {
        for (const p of points) if (p) this._point.price = p.price;
        this.requestUpdate();
    }

    updateAllViews() {
        this._paneViews.forEach((pw) => pw.update());
        this._priceAxisViews.forEach((tw) => tw.update());
    }

    priceAxisViews() {
        return this._priceAxisViews;
    }

    _moveToState(state: InteractionState) {
        switch(state) {
            case InteractionState.NONE:
                document.body.style.cursor = "default";
                this._unsubscribe("mousedown", this._handleMouseDownInteraction);
                break;

            case InteractionState.HOVERING:
                document.body.style.cursor = "pointer";
                this._unsubscribe("mouseup", this._childHandleMouseUpInteraction);
                this._subscribe("mousedown", this._handleMouseDownInteraction)
                this.chart.applyOptions({handleScroll: true});
                break;

            case InteractionState.DRAGGING:
                document.body.style.cursor = "grabbing";
                this._subscribe("mouseup", this._childHandleMouseUpInteraction);
                this.chart.applyOptions({handleScroll: false});
                break;
        }
        this._state = state;
    }

    _onDrag(diff: any) {
        this._addDiffToPoint(this._point, 0, diff.price);
        this.requestUpdate();
    }

    _mouseIsOverDrawing(param: MouseEventParams, tolerance = 4) {
        if (!param.point) return false;
        const y = this.series.priceToCoordinate(this._point.price);
        if (!y) return false;
        return (Math.abs(y-param.point.y) < tolerance);
    }

    protected _onMouseDown() {
        this._startDragPoint = null;
        const hoverPoint = this._latestHoverPoint;
        if (!hoverPoint) return;
        return this._moveToState(InteractionState.DRAGGING);
    }

    protected async _childHandleMouseUpInteraction(): Promise<void> {
        this._handleMouseUpInteraction();
        window.pythonObject.log_message(`Moved ${this._point.quantity} of ${this._point.ticker} to price: ${this._point.price}`);
        window.pythonObject.handleCancelOrder(this._point.orderId, this._point.permId, this._point.clientId);
        let update = true;
        const result = await window.pythonObject.handleHorizontalLineOrder(this._point.price, this._point.operation, this._point.quantity, update);
        const data = JSON.parse(result);
    
        const { orderId, permId, clientId, operation} = data;
        console.log('order id:', orderId, 'perm id:', permId, 'client id:', clientId, 'operation:', operation);
        this._point.orderId = orderId;
        this._point.permId = permId;
        this._point.clientId = clientId;
        this._point.operation = operation;

        this.saveDrawings();

        if (!this._callbackName) return;
        window.callbackFunction(`${this._callbackName}_~_${this._point.price.toFixed(8)}`);
    }
}