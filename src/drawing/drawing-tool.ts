import {
    IChartApi,
    ISeriesApi,
    Logical,
    MouseEventParams,
    SeriesType,
} from 'lightweight-charts';
import { Drawing } from './drawing';
import { HorizontalLine } from '../horizontal-line/horizontal-line';

declare global {
    interface Window {
        pythonObject: any; 
    }
}

export class DrawingTool {
    private _chart: IChartApi;
    private _series: ISeriesApi<SeriesType>;
    private _finishDrawingCallback: Function | null = null;

    private _drawings: Drawing[] = [];
    private _activeDrawing: Drawing | null = null;
    private _isDrawing: boolean = false;
    private _drawingType: (new (...args: any[]) => Drawing) | null = null;

    constructor(chart: IChartApi, series: ISeriesApi<SeriesType>, private saveDrawings: Function, finishDrawingCallback: Function | null = null) {
        this._chart = chart;
        this._series = series;
        this._finishDrawingCallback = finishDrawingCallback;

        this._chart.subscribeClick(this._clickHandler);
        this._chart.subscribeCrosshairMove(this._moveHandler);
    }

    private _clickHandler = (param: MouseEventParams) => this._onClick(param);
    private _moveHandler = (param: MouseEventParams) => this._onMouseMove(param);

    beginDrawing(DrawingType: new (...args: any[]) => Drawing) {
        this._drawingType = DrawingType;
        this._isDrawing = true;
    }

    stopDrawing() {
        this._isDrawing = false;
        this._activeDrawing = null;
    }

    get drawings() {
        return this._drawings;
    }

    addNewDrawing(drawing: Drawing) {
        this._series.attachPrimitive(drawing);
        this._drawings.push(drawing);
    }

    delete(d: Drawing | null) {
        if (d == null) return;
        const idx = this._drawings.indexOf(d);
        if (idx == -1) return;
        this._drawings.splice(idx, 1)
        d.detach();
    }

    clearDrawings() {
        for (const d of this._drawings) d.detach();
        this._drawings = [];
    }

    repositionOnTime() {
        for (const drawing of this.drawings) {
            const newPoints = []
            for (const point of drawing.points) {
                if (!point) {
                    newPoints.push(point);
                    continue;
                }
                const logical = point.time ? this._chart.timeScale()
                    .coordinateToLogical(
                        this._chart.timeScale().timeToCoordinate(point.time) || 0
                    ) : point.logical;
                newPoints.push({
                    time: point.time,
                    logical: logical as Logical,
                    price: point.price,
                })
            }
            drawing.updatePoints(...newPoints);
        }
    }

    private async _onClick(param: MouseEventParams) {
        if (!this._isDrawing) return;

        const point = await Drawing._addEventToPoint(param, this._series);
        if (!point) return;

        if (this._activeDrawing == null) {
            if (this._drawingType == null) return;

            // this._activeDrawing = new this._drawingType(point, point);
            // this._series.attachPrimitive(this._activeDrawing);
            if (this._drawingType == HorizontalLine) {
                let update = false
                const result = await window.pythonObject.handleHorizontalLineOrder(point.price, '', 0, update);
                const data = JSON.parse(result);
    
                const { orderId, permId, clientId, operation} = data;
                console.log('order id:', orderId, 'perm id:', permId, 'client id:', clientId, 'operation:', operation);
                point.orderId = orderId;
                point.permId = permId;
                point.clientId = clientId;
                point.operation = operation;

                const operationColor = point.operation === 'Buy' ? 'rgba(72, 222, 14, 1)' : point.operation === 'Sell' ? 'rgba(181, 9, 17, 1)' : '#1E80F0';

                this._activeDrawing = new this._drawingType(point, point, this.saveDrawings);
                this._activeDrawing.applyOptions({lineColor: operationColor});
                this._series.attachPrimitive(this._activeDrawing);

                window.pythonObject.log_message(`Added horizontal line at price: ${point.price}`);
                window.pythonObject.log_message(`${point.operation} ${point.quantity} of ${point.ticker} at ${point.price}`);
                
                this._onClick(param);
            } else {
                this._activeDrawing = new this._drawingType(point, point, this.saveDrawings);
                this._series.attachPrimitive(this._activeDrawing);
            }
        }
        else {
            this._drawings.push(this._activeDrawing);
            this.stopDrawing();

            if (!this._finishDrawingCallback) return;
            this._finishDrawingCallback();
        }
    }

    private _onMouseMove(param: MouseEventParams) {
        if (!param) return;

        for (const t of this._drawings) t._handleHoverInteraction(param);

        if (!this._isDrawing || !this._activeDrawing) return;

        const point = Drawing._eventToPoint(param, this._series);
        if (!point) return;
        this._activeDrawing.updatePoints(null, point);
        // this._activeDrawing.setSecondPoint(point);
    }
}