import React, { useEffect } from 'react'
import Chart from "react-apexcharts";

const ApexChart = ({ data }) => {

	console.log(data);

	useEffect(() => {
		// ApexCharts.exec('realtime', 'updateSeries', [{
		// 	data: data
		//   }])
	}, [data]);


    return (
        <div>
            <Chart
                type="area"
                height={300}
                width='100%'
                series={[
                    {
                        name: "BTC",
                        data: data
                    }
                ]}

                options={{
                    chart: {
                        toolbar: {
                            show: false
                        },

                    },
                    colors: ['#f90000'],
                    stroke: { width: 1, curve: 'smooth' },
                    dataLabels: { enabled: false },
                    // xaxis: {
                    //     categories: data?.map(data => data.time),

                    // },
                    yaxis: {
                        show: false,
                    }
                }}
            />
        </div>
    )
}

export default ApexChart
